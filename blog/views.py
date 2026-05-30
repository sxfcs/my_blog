from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Article

def article_list(request):
    articles = Article.objects.all()
    query = request.GET.get('q', '')  # 获取搜索关键词
    
    if query:
        # 同时搜索标题和内容
        articles = articles.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    return render(request, 'blog/article_list.html', {
        'articles': articles,
        'query': query,  # 把关键词传回模板，用于保留输入框内容
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