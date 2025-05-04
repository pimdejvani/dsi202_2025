from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),         # ถ้าเข้า /admin/ → ไปยัง admin ของ Django
    path('', include('myapp.urls')),         # ถ้าเข้า root URL ทั้งหมด → ให้ดูใน myapp/urls.py
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.BASE_DIR / 'static'
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )