from django.contrib import admin
from .models import Article, Category, Topic, Reply  # 添加 Topic, Reply 导入
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# 定义导入导出配置
class ArticleResource(resources.ModelResource):
    class Meta:
        model = Article
        import_id_fields = ['title']


# 分类后台管理
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_time']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


# 文章后台管理
@admin.register(Article)
class ArticleAdmin(ImportExportModelAdmin):
    resource_class = ArticleResource
    list_display = ['title', 'category', 'total_views', 'created_time']
    list_filter = ['category', 'created_time']
    search_fields = ['title']


# ========== 新增：讨论区后台管理 ==========

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'view_count', 'created_time']
    list_filter = ['created_time', 'author']
    search_fields = ['title', 'content']
    raw_id_fields = ['author', 'article']  # 作者和关联文章显示为搜索框
    date_hierarchy = 'created_time'  # 日期层级筛选


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['topic', 'author', 'created_time']
    list_filter = ['created_time', 'author']
    search_fields = ['content']
    raw_id_fields = ['author', 'topic']