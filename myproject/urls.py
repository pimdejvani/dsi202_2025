from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # ถ้ามีหน้าเว็บของ myapp ให้เพิ่มบรรทัดนี้ (ไม่จำเป็นถ้าแอปไม่มี view)
    path('', include('myapp.urls')),
]

# ในโหมด DEBUG ให้ Django ให้บริการไฟล์ใน MEDIA_ROOT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
