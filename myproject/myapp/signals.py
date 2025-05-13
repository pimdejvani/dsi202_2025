from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User
from .models import Student

@receiver(user_signed_up)
def create_student_on_signup(sender, request, user, **kwargs):
    # เช็คว่าผู้ใช้ใหม่ได้ถูกสร้างหรือไม่
    if user:
        # ตรวจสอบว่า Student ที่มี email นี้มีอยู่แล้วหรือไม่
        student, created = Student.objects.get_or_create(
            email=user.email,  # ใช้ email ในการเชื่อมโยง
            defaults={
                'username': '',
                'birth': None,  # กรอก None หรือค่าเริ่มต้น
                'level': '',  # ค่าเริ่มต้น
                'grade': '',  # ค่าเริ่มต้น
                'degree': '',  # ค่าเริ่มต้น
                'interest': '',  # ค่าเริ่มต้น
                'profile_picture': None  # รูปโปรไฟล์จะถูกสร้างขึ้นในภายหลัง
            }
        )
        
        if created:
            # ถ้าแถวใหม่ถูกสร้างขึ้น
            print("Student created for", user.email)
        else:
            # ถ้าแถวที่มีอยู่แล้วถูกใช้
            print("Student already exists for", user.email)