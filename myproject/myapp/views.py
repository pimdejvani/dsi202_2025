from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import CampForm


from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'myapp/account/login.html'





from allauth.account.views import SignupView
from django.shortcuts import redirect
from django.conf import settings 

class CustomSignupView(SignupView):
    def form_valid(self, form):
        # เมื่อฟอร์มสมัครสมาชิกถูกต้อง
        super().form_valid(form)
        # ใช้ ACCOUNT_SIGNUP_REDIRECT_URL จาก settings.py หรือกำหนด URL ที่ต้องการ
        redirect_url = 'http://localhost:8000/peddlecamp/'
        
        return redirect(redirect_url)  # รีไดเร็กต์ไปที่ URL ที่กำหนด


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

    def get(self, request, *args, **kwargs):
        print('------ get')
        form = CampForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        print('------ post')
        form = CampForm(request.POST, request.FILES)
        if form.is_valid():
            print('------ form valid')
            form.save()  # บันทึกข้อมูลลงในฐานข้อมูล
            return redirect('myapp:promote-done')  # เปลี่ยนไปยังหน้า 'done'
        else:
            print('------ form errors:', form.errors)  # พิมพ์ข้อผิดพลาดของฟอร์ม
        return self.render_to_response({'form': form})

# 7. โปรโมทกิจกรรม - เสร็จสิ้น
class PromoteDonePageView(TemplateView):
    template_name = 'myapp/promote_done.html'