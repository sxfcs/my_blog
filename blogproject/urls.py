from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # 新增
from django.conf.urls.static import static  # 新增

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('mdeditor/', include('mdeditor.urls')),  # 处理图片上传等功能
    path('comment/', include('comment.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)