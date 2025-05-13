from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import CampForm ,StudentProfileForm
from .models import Student


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ตรวจสอบว่า User(ผู้ใช้) ได้ทำการสมัครแล้ว และมีข้อมูล Class Student หรือไม่
        if self.request.user.is_authenticated:
            try:
                # ดึงข้อมูล Class Student โดยใช้ email ของ User(ผู้ใช้)
                student = Student.objects.get(email=self.request.user.email)  # ใช้ email เพื่อเชื่อมโยง
                form = StudentProfileForm(instance=student)  # สร้างฟอร์มเพื่อแสดงข้อมูลในแบบฟอร์ม
                context['form'] = form
                print("------ # ข้อมูล Class Student ถูกดึงสำเร็จสำหรับ User(ผู้ใช้)")
            except Student.DoesNotExist:
                # หากไม่พบข้อมูล Class Student จะไม่รีไดเร็กต์อีกแล้ว
                print("------ # ไม่พบข้อมูล Class Student สำหรับ User(ผู้ใช้)")
                context['form'] = None  # หรือส่งฟอร์มใหม่หากต้องการให้ผู้ใช้กรอกข้อมูล
                context['error'] = "ไม่พบข้อมูลโปรไฟล์ของคุณ"

        else:
            print("------ # User(ผู้ใช้) ยังไม่ได้เข้าสู่ระบบ")
            return redirect('login')  # ถ้าไม่ได้ล็อกอินให้รีไดเร็กต์ไปหน้า login

        return context

    def post(self, request, *args, **kwargs):
        # ตรวจสอบว่า User(ผู้ใช้) ได้ทำการสมัครแล้ว และมีข้อมูล Class Student หรือไม่
        if request.user.is_authenticated:
            try:
                student = Student.objects.get(email=request.user.email)  # ใช้ email เพื่อเชื่อมโยง
            except Student.DoesNotExist:
                print("------ # ไม่พบข้อมูล Class Student สำหรับ User(ผู้ใช้)")
                return redirect('myapp:profile')  # ถ้าไม่พบข้อมูล Class Student

            # ประมวลผลฟอร์มที่ถูกส่งมาจากผู้ใช้
            form = StudentProfileForm(request.POST, request.FILES, instance=student)
            if form.is_valid():
                form.save()  # บันทึกข้อมูล
                print("------ # ข้อมูลถูกบันทึกเรียบร้อย")
                return redirect('myapp:profile')  # รีไดเร็กต์กลับไปที่หน้าโปรไฟล์หลังบันทึกข้อมูล
            else:
                print("------ # ฟอร์มข้อมูลไม่ถูกต้อง")
        else:
            print("------ # User(ผู้ใช้) ยังไม่ได้เข้าสู่ระบบ")
            return redirect('login')  # ถ้าไม่ใช่ผู้ใช้ที่ล็อกอินแล้วให้รีไดเร็กต์ไปที่หน้า login
        

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