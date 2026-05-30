from django.contrib import admin
from .models import Article, Category  # 导入 Category
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# 定义导入导出配置
class ArticleResource(resources.ModelResource):
    class Meta:
        model = Article
        # 用标题作为唯一标识，避免重复导入
        import_id_fields = ['title']

# 分类后台管理（新增）
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_time']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}  # 根据名称自动生成 slug

# 注册后台，使用带导入导出功能的Admin
@admin.register(Article)
class ArticleAdmin(ImportExportModelAdmin):
    resource_class = ArticleResource
    list_display = ['title', 'category', 'total_views', 'created_time']  # 添加分类和浏览量
    list_filter = ['category', 'created_time']  # 添加分类筛选器
    search_fields = ['title']