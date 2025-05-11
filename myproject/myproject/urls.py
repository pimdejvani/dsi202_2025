from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from myapp.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),         # ถ้าเข้า /admin/ → ไปยัง admin ของ Django
    path('', include('myapp.urls')),         # ถ้าเข้า root URL ทั้งหมด → ให้ดูใน myapp/urls.py
    path('accounts/', include('allauth.urls')),  # เชื่อมต่อ Allauth URLs
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
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