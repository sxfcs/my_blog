from django.db import models
from django.utils import timezone
from mdeditor.fields import MDTextField  # ← 添加这一行导入

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = MDTextField(verbose_name='内容')  # ← 把 TextField 改成 MDTextField
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # 新增：浏览量字段，默认值为0
    total_views = models.PositiveIntegerField(default=0, verbose_name='浏览量')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']  # 按时间倒序排列
        verbose_name = '文章'
        verbose_name_plural = '文章'
