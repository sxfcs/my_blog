from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from mdeditor.fields import MDTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User  # 新增：导入用户模型
from comment.models import Comment
import markdown

# 分类模型
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='分类名称', unique=True)
    slug = models.SlugField(max_length=50, verbose_name='URL标识', unique=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# 文章模型
class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = MDTextField(verbose_name='内容')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    total_views = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True, 
        verbose_name='分类'
    )
    
    comments = GenericRelation(Comment)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.content and not self.content.strip().startswith('<'):
            self.content = markdown.markdown(self.content, extensions=['extra', 'codehilite'])
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_time']
        verbose_name = '文章'
        verbose_name_plural = '文章'


# ========== 新增：讨论区模型 ==========

class Topic(models.Model):
    """讨论主题"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    view_count = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    
    # 可选：关联到文章（让讨论区可以围绕某篇文章）
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        verbose_name='关联文章'
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_time']
        verbose_name = '讨论主题'
        verbose_name_plural = '讨论主题'


class Reply(models.Model):
    """主题下的回复"""
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='replies', verbose_name='所属主题')
    
    def __str__(self):
        return f'回复 #{self.pk}: {self.content[:30]}'
    
    class Meta:
        ordering = ['created_time']
        verbose_name = '回复'
        verbose_name_plural = '回复'