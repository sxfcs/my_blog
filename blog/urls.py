from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # 原有路由
    path('', views.article_list, name='article_list'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    
    # ========== 讨论区路由 ==========
    # 列表和新建
    path('forum/', views.forum_list, name='forum_list'),
    path('forum/new/', views.forum_new, name='forum_new'),
    
    # 主题详情
    path('forum/<int:pk>/', views.forum_detail, name='forum_detail'),
    
    # 主题编辑/删除
    path('forum/topic/<int:pk>/edit/', views.forum_topic_edit, name='forum_topic_edit'),
    path('forum/topic/<int:pk>/delete/', views.forum_topic_delete, name='forum_topic_delete'),
    
    # 回复编辑/删除
    path('forum/reply/<int:pk>/edit/', views.forum_reply_edit, name='forum_reply_edit'),
    path('forum/reply/<int:pk>/delete/', views.forum_reply_delete, name='forum_reply_delete'),
    
    # 用户注册
    path('register/', views.register, name='register'),

    # 用户退出
    path('logout/', views.user_logout, name='logout'),

    path('login/', views.user_login, name='login'),

]