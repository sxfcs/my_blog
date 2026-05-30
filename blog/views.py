from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Article, Category  # 添加 Category 导入

def article_list(request):
    articles = Article.objects.all()
    query = request.GET.get('q', '')  # 获取搜索关键词
    category_slug = request.GET.get('category', '')  # 获取分类参数
    
    # 按分类筛选
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        articles = articles.filter(category=current_category)
    
    # 按关键词搜索
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    # 获取所有分类（用于导航栏）
    categories = Category.objects.all()
    
    return render(request, 'blog/article_list.html', {
        'articles': articles,
        'query': query,
        'categories': categories,
        'current_category': current_category,  # 当前选中的分类
    })

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    # 使用 cookie 判断是否已经计数
    cookie_key = f'article_{pk}_viewed'
    if not request.COOKIES.get(cookie_key):
        article.total_views += 1
        article.save(update_fields=['total_views'])
        
    response = render(request, 'blog/article_detail.html', {'article': article})
    
    # 设置 cookie，24小时内不再重复计数
    if not request.COOKIES.get(cookie_key):
        response.set_cookie(cookie_key, 'true', max_age=86400)
    
    return response