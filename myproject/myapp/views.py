from django.views.generic import TemplateView

# 1. หน้าแรก
class HomePageView(TemplateView):
    template_name = 'myapp/home.html'


# 2. หน้าประเภทค่าย (health, engineer, …, date)
class HealthCampView(TemplateView):
    template_name = 'myapp/category_health.html'

class EngineerCampView(TemplateView):
    template_name = 'myapp/category_engineer.html'

class LanguageCampView(TemplateView):
    template_name = 'myapp/category_language.html'

class ArchitectureCampView(TemplateView):
    template_name = 'myapp/category_architecture.html'

class VolunteerCampView(TemplateView):
    template_name = 'myapp/category_volunteer.html'

class DigitalItCampView(TemplateView):
    template_name = 'myapp/category_digital_it.html'

class OtherCampView(TemplateView):
    template_name = 'myapp/category_other.html'

class DateCampView(TemplateView):
    template_name = 'myapp/category_date.html'


# 3. หน้าค้นหาตัวตน
class PersonalizePageView(TemplateView):
    template_name = 'myapp/personalize.html'


# 4. หน้าโปรไฟล์
class ProfilePageView(TemplateView):
    template_name = 'myapp/profile.html'


# 5. โปรโมทกิจกรรม - เริ่มต้น
class PromoteStartPageView(TemplateView):
    template_name = 'myapp/promote_start.html'


# 6. โปรโมทกิจกรรม - ฟอร์ม
class PromoteFormPageView(TemplateView):
    template_name = 'myapp/promote_form.html'


# 7. โปรโมทกิจกรรม - เสร็จสิ้น
class PromoteDonePageView(TemplateView):
    template_name = 'myapp/promote_done.html'