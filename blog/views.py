from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from .models import Article, Category, Topic, Reply
from .forms import TopicForm, ReplyForm, UserRegisterForm


def article_list(request):
    articles = Article.objects.all()
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        articles = articles.filter(category=current_category)
    
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    categories = Category.objects.all()
    
    # 获取侧边栏数据
    latest_topics = Topic.objects.all().order_by('-created_time')[:5]
    hot_topics = Topic.objects.all().order_by('-view_count')[:5]
    
    return render(request, 'blog/article_list.html', {
        'articles': articles,
        'query': query,
        'categories': categories,
        'current_category': current_category,
        'latest_topics': latest_topics,
        'hot_topics': hot_topics,
    })


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    cookie_key = f'article_{pk}_viewed'
    if not request.COOKIES.get(cookie_key):
        article.total_views += 1
        article.save(update_fields=['total_views'])
        
    response = render(request, 'blog/article_detail.html', {'article': article})
    
    if not request.COOKIES.get(cookie_key):
        response.set_cookie(cookie_key, 'true', max_age=86400)
    
    return response


# ========== 讨论区视图 ==========

def forum_list(request):
    """讨论区首页：显示所有主题"""
    topics = Topic.objects.all()
    query = request.GET.get('q', '')
    
    if query:
        topics = topics.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    paginator = Paginator(topics, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/forum_list.html', {
        'topics': page_obj,
        'query': query,
    })


def forum_detail(request, pk):
    """主题详情页：显示主题内容和所有回复"""
    topic = get_object_or_404(Topic, pk=pk)
    
    # 增加浏览量
    topic.view_count += 1
    topic.save(update_fields=['view_count'])
    
    replies = topic.replies.all()
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.topic = topic
            reply.save()
            return redirect('blog:forum_detail', pk=pk)
    else:
        form = ReplyForm()
    
    return render(request, 'blog/forum_detail.html', {
        'topic': topic,
        'replies': replies,
        'form': form,
    })


@login_required
def forum_new(request):
    """新建主题"""
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect('blog:forum_detail', pk=topic.pk)
    else:
        form = TopicForm()
    
    articles = Article.objects.all()
    form.fields['article'].choices = [('', '无')] + [(a.id, a.title) for a in articles]
    
    return render(request, 'blog/forum_new.html', {
        'form': form,
    })


@login_required
def forum_topic_edit(request, pk):
    """编辑主题"""
    topic = get_object_or_404(Topic, pk=pk)
    
    if topic.author != request.user and not request.user.is_staff:
        return redirect('blog:forum_detail', pk=pk)
    
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('blog:forum_detail', pk=pk)
    else:
        form = TopicForm(instance=topic)
    
    articles = Article.objects.all()
    form.fields['article'].choices = [('', '无')] + [(a.id, a.title) for a in articles]
    
    return render(request, 'blog/forum_new.html', {'form': form})


@login_required
def forum_topic_delete(request, pk):
    """删除主题"""
    topic = get_object_or_404(Topic, pk=pk)
    
    if topic.author != request.user and not request.user.is_staff:
        return redirect('blog:forum_detail', pk=pk)
    
    topic.delete()
    return redirect('blog:forum_list')


@login_required
def forum_reply_edit(request, pk):
    """编辑回复"""
    reply = get_object_or_404(Reply, pk=pk)
    
    if reply.author != request.user and not request.user.is_staff:
        return redirect('blog:forum_detail', pk=reply.topic.pk)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            return redirect('blog:forum_detail', pk=reply.topic.pk)
    else:
        form = ReplyForm(instance=reply)
    
    return render(request, 'blog/forum_reply_edit.html', {
        'form': form,
        'reply': reply,
    })


@login_required
def forum_reply_delete(request, pk):
    """删除回复"""
    reply = get_object_or_404(Reply, pk=pk)
    topic_pk = reply.topic.pk
    
    if reply.author != request.user and not request.user.is_staff:
        return redirect('blog:forum_detail', pk=topic_pk)
    
    reply.delete()
    return redirect('blog:forum_detail', pk=topic_pk)


# ========== 用户注册、登录、退出视图 ==========

def register(request):
    """用户注册，注册成功后自动加入普通用户组"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # 将用户添加到"普通用户"组
            group, created = Group.objects.get_or_create(name='普通用户')
            user.groups.add(group)
            
            # 注册后自动登录
            login(request, user)
            return redirect('blog:article_list')
    else:
        form = UserRegisterForm()
    
    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    """用户登录视图"""
    if request.user.is_authenticated:
        return redirect('blog:article_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'🎉 {username}，欢迎回来！')
                return redirect('blog:article_list')
            else:
                messages.error(request, '用户名或密码错误，请重试')
        else:
            messages.error(request, '请输入用户名和密码')
    
    return render(request, 'blog/login.html')


def user_logout(request):
    """自定义退出登录视图"""
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f'👋 {username}，您已成功退出登录')
    else:
        messages.info(request, '您尚未登录')
    
    return redirect('blog:article_list')