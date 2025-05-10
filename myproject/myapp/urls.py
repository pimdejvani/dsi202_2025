# myapp/urls.py

from django.urls import path
from .views import (
    HomePageView,
    PersonalizePageView,
    ProfilePageView,
    PromoteStartPageView,
    PromoteFormPageView,
    PromoteDonePageView, 
    HealthCampView, EngineerCampView, LanguageCampView,
    ArchitectureCampView, VolunteerCampView, DigitalItCampView, DateCampView,
)
from myapp.views import CustomSignupView


app_name = 'myapp'

urlpatterns = [
    path('accounts/signup/', CustomSignupView.as_view(), name='signup'),
    # 1. หน้าแรก
    path('peddlecamp/', HomePageView.as_view(), name='home'),

    # แยก URL & View ของแต่ละประเภท
    path('peddlecamp/health/', HealthCampView.as_view(), name='camp-health'),
    path('peddlecamp/engineer/', EngineerCampView.as_view(), name='camp-engineer'),
    path('peddlecamp/language/', LanguageCampView.as_view(), name='camp-language'),
    path('peddlecamp/architecture/', ArchitectureCampView.as_view(), name='camp-architecture'),
    path('peddlecamp/volunteer/', VolunteerCampView.as_view(), name='camp-volunteer'),
    path('peddlecamp/digital_it/', DigitalItCampView.as_view(), name='camp-digital_it'),

    # หน้า date (เข้าจากหน้าแรกเท่านั้น)
    path('peddlecamp/date/', DateCampView.as_view(), name='camp-date'),
    # 3. หน้าค้นหาตัวตน
    path('peddlecamp/personalize_camp/', 
         PersonalizePageView.as_view(), 
         name='personalize-camp'),

    # 4. หน้าโปรไฟล์
    path('peddlecamp/profile/', 
         ProfilePageView.as_view(), 
         name='profile'),

    # 5. โปรโมทกิจกรรม – เริ่มต้น
    path('peddlecamp/promote_camp/', 
         PromoteStartPageView.as_view(), 
         name='promote-start'),
    # 6. โปรโมทกิจกรรม – ฟอร์ม
    path('peddlecamp/promote_camp/forms/', 
         PromoteFormPageView.as_view(), 
         name='promote-form'),
    # 7. โปรโมทกิจกรรม – เสร็จสิ้น
    path('peddlecamp/promote_camp/forms/done/', 
         PromoteDonePageView.as_view(), 
         name='promote-done'),
]
