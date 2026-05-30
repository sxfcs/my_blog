from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from mdeditor.fields import MDTextField
from django.contrib.contenttypes.fields import GenericRelation  # 新增导入
from comment.models import Comment  # 新增导入

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
        # 自动生成 slug（用于 URL）
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
    
    # 分类外键（一个分类对应多篇文章）
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,  # 删除分类时，文章分类设为空
        null=True, 
        blank=True, 
        verbose_name='分类'
    )
    
    # 新增：评论关联字段
    comments = GenericRelation(Comment)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']  # 按时间倒序排列
        verbose_name = '文章'
        verbose_name_plural = '文章'