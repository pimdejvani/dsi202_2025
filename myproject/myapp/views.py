from django.views.generic import TemplateView , View
from django.shortcuts import render, redirect
from .forms import CampForm ,StudentProfileForm
from .models import Student,Camp
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from datetime import datetime, date
from django.contrib.auth.views import LoginView
import re
import ast

from django.contrib import messages

from allauth.account.views import SignupView
from django.shortcuts import redirect
from django.conf import settings 




class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'




class CustomSignupView(SignupView):
    def form_valid(self, form):
        # เมื่อฟอร์มสมัครสมาชิกถูกต้อง
        super().form_valid(form)
        # ใช้ ACCOUNT_SIGNUP_REDIRECT_URL จาก settings.py หรือกำหนด URL ที่ต้องการ
        redirect_url = 'http://localhost:8000/peddlecamp/'
        
        return redirect(redirect_url)  # รีไดเร็กต์ไปที่ URL ที่กำหนด


from django.utils import timezone

# 1. หน้าแรก
# ตัวอย่างใน view.py
class HomePageView(TemplateView):
    template_name = 'myapp/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Slider ตามวันที่ใกล้หมดเขต (เรียง final_date น้อยสุดก่อน)
        camps = Camp.objects.filter(
            prove=True,
            final_date__gte=timezone.now().date()
        ).order_by('final_date')[:7]
        context['slider_camps'] = camps

        # 2. Slider ตาม id มากสุด (ค่ายล่าสุด)
        camps_by_id = Camp.objects.filter(
            prove=True,
            final_date__gte=timezone.now().date()
        ).order_by('-id')[:7]
        context['slider_camps_by_id'] = camps_by_id

        # 3. เตรียมค่าจาก Student (กรณี login)
        student_birth = ""
        student_level = ""
        student_grade = ""
        student_degree = ""
        student_interest = ""
        personalized_camps = []
        slider_camps_interest = []

        if self.request.user.is_authenticated:
            student = Student.objects.filter(email=self.request.user.email).first()
            if student:
                # วันเกิดเป็น string สำหรับ JS
                student_birth = student.birth.strftime('%Y-%m-%d') if student.birth else ""
                student_level = student.level if student.level else ""
                student_grade = student.grade if student.grade else ""
                student_degree = student.degree if student.degree else ""
                student_interest = student.interest if student.interest else ""

                # 3. Personalized: เฉพาะ student ที่มีวันเกิด (อายุ >= min_age ตอนถึงวัน final_date)
                if student.birth:
                    today = timezone.now().date()
                    birth_date = student.birth
                    camps_p = Camp.objects.filter(
                        prove=True,
                        final_date__gte=today
                    ).order_by('-id')
                    def calculate_age(birth, ref_date):
                        return ref_date.year - birth.year - ((ref_date.month, ref_date.day) < (birth.month, birth.day))
                    filtered = []
                    for camp in camps_p:
                        age_at_final = calculate_age(birth_date, camp.final_date)
                        if camp.min_age is not None and age_at_final >= camp.min_age:
                            filtered.append(camp)
                    personalized_camps = filtered[:7]  # แสดง 7 อันดับ

                # 4. Slider: ตาม interest (keyword matching)
                interest = student.interest or ""
                camp_results = list(
                    Camp.objects.filter(
                        prove=True,
                        final_date__gte=timezone.now().date()
                    ).order_by('-id')[:30]  # เผื่อไว้เยอะๆก่อน
                )

                keywords = []
                if interest:
                    try:
                        if interest.strip().startswith("["):
                            items = ast.literal_eval(interest)
                            if isinstance(items, list):
                                for item in items:
                                    if isinstance(item, dict) and 'value' in item:
                                        keywords.append(item['value'].strip())
                                    elif isinstance(item, str):
                                        keywords.append(item.strip())
                        else:
                            keywords = [x.strip() for x in interest.split(',') if x.strip()]
                    except Exception:
                        keywords = [x.strip() for x in interest.split(',') if x.strip()]

                def keyword_count(camp, keywords):
                    found = set()
                    texts = [(camp.detail_activity or ""), (camp.description_camp or "")]
                    for kw in keywords:
                        for txt in texts:
                            if kw and re.search(re.escape(kw), txt, re.IGNORECASE):
                                found.add(kw)
                    return len(found)

                if keywords:
                    camp_results = sorted(
                        camp_results,
                        key=lambda camp: (keyword_count(camp, keywords), camp.id),
                        reverse=True
                    )
                else:
                    camp_results = sorted(camp_results, key=lambda camp: camp.id, reverse=True)
                slider_camps_interest = camp_results[:7]

        # --- ใส่ลง context ---
        context['student_birth'] = student_birth
        context['student_level'] = student_level
        context['student_grade'] = student_grade
        context['student_degree'] = student_degree
        context['student_interest'] = student_interest
        context['slider_camps_personal'] = personalized_camps  # เงื่อนไขอายุ
        context['slider_camps_interest'] = slider_camps_interest  # match keyword
        print('slider_camps_persona',context['slider_camps_personal'])
        print('slider_camps_interest',context['slider_camps_interest'])
        return context

# 2. หน้าประเภทค่าย (health, engineer, …, date)
class HealthCampView(TemplateView):
    template_name = 'myapp/category_health.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()
        upcoming = Camp.objects.filter(prove=True, final_date__gte=today ,typeof_camp='health').order_by('final_date')
        expired = Camp.objects.filter(prove=True, final_date__lt=today ,typeof_camp='health').order_by('-final_date')
        all_camps = list(upcoming) + list(expired)

        context['all_camps'] = all_camps
        print(context['all_camps'])

        return context

class EngineerCampView(TemplateView):
    template_name = 'myapp/category_engineer.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()
        upcoming = Camp.objects.filter(prove=True, final_date__gte=today ,typeof_camp='engineer').order_by('final_date')
        expired = Camp.objects.filter(prove=True, final_date__lt=today ,typeof_camp='engineer').order_by('-final_date')
        all_camps = list(upcoming) + list(expired)

        context['all_camps'] = all_camps
        print(context['all_camps'])

        return context

class LanguageCampView(TemplateView):
    template_name = 'myapp/category_language.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()
        upcoming = Camp.objects.filter(prove=True, final_date__gte=today ,typeof_camp='language').order_by('final_date')
        expired = Camp.objects.filter(prove=True, final_date__lt=today ,typeof_camp='language').order_by('-final_date')
        all_camps = list(upcoming) + list(expired)

        context['all_camps'] = all_camps
        print(context['all_camps'])

        return context
    
class ArchitectureCampView(TemplateView):
    template_name = 'myapp/category_architecture.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()
        upcoming = Camp.objects.filter(prove=True, final_date__gte=today ,typeof_camp='architecture').order_by('final_date')
        expired = Camp.objects.filter(prove=True, final_date__lt=today ,typeof_camp='architecture').order_by('-final_date')
        all_camps = list(upcoming) + list(expired)

        context['all_camps'] = all_camps
        print(context['all_camps'])

        return context

class VolunteerCampView(TemplateView):
    template_name = 'myapp/category_volunteer.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()
        upcoming = Camp.objects.filter(prove=True, final_date__gte=today ,typeof_camp='volunteer').order_by('final_date')
        expired = Camp.objects.filter(prove=True, final_date__lt=today ,typeof_camp='volunteer').order_by('-final_date')
        all_camps = list(upcoming) + list(expired)

        context['all_camps'] = all_camps
        print(context['all_camps'])

        return context

class DigitalItCampView(TemplateView):
    template_name = 'myapp/category_digital_it.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()
        upcoming = Camp.objects.filter(prove=True, final_date__gte=today ,typeof_camp='digital_it').order_by('final_date')
        expired = Camp.objects.filter(prove=True, final_date__lt=today ,typeof_camp='digital_it').order_by('-final_date')
        all_camps = list(upcoming) + list(expired)

        context['all_camps'] = all_camps
        print(context['all_camps'])

        return context

class OtherCampView(TemplateView):
    template_name = 'myapp/category_other.html'

class DateCampView(TemplateView):
    template_name = 'myapp/category_date.html'


class PersonalizePageView(TemplateView):
    template_name = 'myapp/personalize.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_camps = Camp.objects.filter(prove=True)
        context['all_camps'] = all_camps
        context['camp_results'] = []

        # Default autofill ว่าง
        context['student_birth'] = ""
        context['student_level'] = ""
        context['student_grade'] = ""
        context['student_degree'] = ""
        context['student_interest'] = ""

        if self.request.method == "POST":
            # ดึงค่าจากฟอร์ม
            birth_str = self.request.POST.get("birth", "")
            level = self.request.POST.get("level", "")
            grade = self.request.POST.get("grade", "")
            degree = self.request.POST.get("degree", "")
            interest = self.request.POST.get("interest", "")

            context['student_birth'] = birth_str
            context['student_level'] = level
            context['student_grade'] = grade
            context['student_degree'] = degree
            context['student_interest'] = interest

            camp_results = []
            today = date.today()

            # ไม่กรอกวันเกิด = อายุ 100 ปี
            if birth_str:
                try:
                    birth = datetime.strptime(birth_str, "%Y-%m-%d").date()
                except Exception:
                    birth = today.replace(year=today.year - 100)
            else:
                birth = today.replace(year=today.year - 100)

            for camp in all_camps:
                if not camp.final_date or camp.final_date < today:
                    continue

                # เช็คอายุ (ถ้ามี min_age)
                age = camp.final_date.year - birth.year - (
                    (camp.final_date.month, camp.final_date.day) < (birth.month, birth.day)
                )
                if camp.min_age is not None and age < camp.min_age:
                    continue

                # ============ เช็คระดับชั้น/เกรด/ปริญญา ============
                if not level:
                    match = True  # ถ้าไม่ได้เลือก level ใดๆ match ทุกค่าย
                else:
                    match = False
                    if level == "primary":
                        if camp.primary:
                            # ถ้ามีช่วง grade
                            if camp.primary_grade_from and camp.primary_grade_to:
                                if grade:
                                    try:
                                        g = int(grade)
                                        if camp.primary_grade_from <= g <= camp.primary_grade_to:
                                            match = True
                                    except Exception:
                                        pass  # ถ้ากรอกผิด format ไม่ match
                                else:
                                    # ไม่กรอก grade (แต่เลือก primary) = match ทุกเกรดในช่วงที่ค่ายรับ
                                    match = True
                            elif camp.primary_grade_condition == 'all':
                                match = True
                    elif level == "secondary":
                        if camp.secondary:
                            if camp.secondary_grade_from and camp.secondary_grade_to:
                                if grade:
                                    try:
                                        g = int(grade)
                                        if camp.secondary_grade_from <= g <= camp.secondary_grade_to:
                                            match = True
                                    except Exception:
                                        pass
                                else:
                                    match = True
                            elif camp.secondary_grade_condition == 'all':
                                match = True
                    elif level == "vocational_minor" and camp.vocational_minor:
                        match = True
                    elif level == "vocational_major" and camp.vocational_major:
                        match = True
                    elif level == "drop" and camp.drop:
                        match = True
                    elif level == "degree" and camp.degree:
                        # ถ้าไม่ได้เลือก degree ให้ match ทุกระดับที่ค่ายรับ
                        if camp.degree_grade_condition == 'all':
                            match = True
                        elif camp.degree_from and camp.degree_to:
                            levels = ['bachelor', 'master', 'doctorate']
                            if degree:
                                try:
                                    user_idx = levels.index(degree)
                                    from_idx = levels.index(camp.degree_from)
                                    to_idx = levels.index(camp.degree_to)
                                    if from_idx <= user_idx <= to_idx:
                                        match = True
                                except Exception:
                                    pass
                            else:
                                # ไม่กรอก degree (แต่เลือก level degree) = match ทุกปริญญาที่ค่ายรับ
                                match = True
                        else:
                            match = True
                    elif level == "other" and camp.other:
                        match = True

                if match:
                    camp_results.append(camp)

            # ============== SORT ตาม interest ==============
            # 1. ดึง interest ออกมาเป็น list ของคำ (tagify ส่ง string แบบ json หรือ comma-separated)
            keywords = []
            if interest:
                try:
                    # ถ้าเป็น list ของ dict [{"value":"TCAS"}, ...]
                    if interest.strip().startswith("["):
                        items = ast.literal_eval(interest)
                        if isinstance(items, list):
                            for item in items:
                                if isinstance(item, dict) and 'value' in item:
                                    keywords.append(item['value'].strip())
                                elif isinstance(item, str):
                                    keywords.append(item.strip())
                    else:
                        keywords = [x.strip() for x in interest.split(',') if x.strip()]
                except Exception:
                    keywords = [x.strip() for x in interest.split(',') if x.strip()]
            def keyword_count(camp, keywords):
                found = set()
                texts = [(camp.detail_activity or ""), (camp.description_camp or "")]
                for kw in keywords:
                    for txt in texts:
                        if kw and re.search(re.escape(kw), txt, re.IGNORECASE):
                            found.add(kw)
                return len(found)

            # 2. sort ตามจำนวน keyword ที่ match (จากมากไปน้อย)
            if keywords:
                camp_results = sorted(
                    camp_results,
                    key=lambda camp: keyword_count(camp, keywords),
                    reverse=True
                )

            context['camp_results'] = camp_results

        elif self.request.user.is_authenticated:
            student = Student.objects.filter(email=self.request.user.email).first()
            if student and student.birth:
                context['student_birth'] = student.birth.strftime('%Y-%m-%d')
            else:
                context['student_birth'] = ""
            context['student_level'] = student.level if student else ""
            context['student_grade'] = student.grade if student else ""
            context['student_degree'] = student.degree if student else ""
            context['student_interest'] = student.interest if student else ""

        return context

    # สำคัญ! ต้อง override post เพื่อให้รับ POST ได้ ไม่ error 405
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

            

class ProfilePageView(TemplateView):
    template_name = 'myapp/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ตรวจสอบว่าล็อกอิน
        if not self.request.user.is_authenticated:
            return redirect('login')

        # พยายามดึง Student
        student = Student.objects.filter(email=self.request.user.email).first()
        if student:
            form = StudentProfileForm(instance=student)
        else:
            form = StudentProfileForm()
            context['error'] = "ไม่พบข้อมูลโปรไฟล์ของคุณ กรุณากรอกใหม่"

        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        # พยายามดึง Student
        student = Student.objects.filter(email=request.user.email).first()
        if student:
            form = StudentProfileForm(request.POST, request.FILES, instance=student)
        else:
            # สร้างใหม่ให้ email ตรงกับ user (เพื่อให้บันทึกได้)
            form = StudentProfileForm(request.POST, request.FILES)
            # ดักกรณี email ไม่กรอก/ไม่ถูกต้อง
            if form.is_valid():
                student = form.save(commit=False)
                student.email = request.user.email
                student.save()
                return redirect('myapp:profile')
        
        if form.is_valid():
            form.save()
            return redirect('myapp:profile')
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


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
    

#รายละเอียดค่าย
class CampDetailView(DetailView):
    model = Camp
    template_name = 'myapp/camp_detail.html'
    context_object_name = 'camp'


from .utils import generate_promptpay_qr_image_base64

def donate(request):
    img_base64 = None
    amount = ""
    error_msg = ""
    if request.method == "POST":
        amount = request.POST.get("amount")
        try:
            img_base64 = generate_promptpay_qr_image_base64(
                mobile="0893280067",
                amount=amount
            )
        except Exception as e:
            error_msg = str(e)
    return render(request, "myapp/donate.html", {
        "img_base64": img_base64,
        "amount": amount,
        "error_msg": error_msg,
    })