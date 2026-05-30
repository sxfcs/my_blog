from django.contrib import admin
from .models import Article
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# 定义导入导出配置
class ArticleResource(resources.ModelResource):
    class Meta:
        model = Article
        # 用标题作为唯一标识，避免重复导入
        import_id_fields = ['title']

# 注册后台，使用带导入导出功能的Admin
@admin.register(Article)
class ArticleAdmin(ImportExportModelAdmin):
    resource_class = ArticleResource
    list_display = ['title', 'created_time']
    search_fields = ['title']