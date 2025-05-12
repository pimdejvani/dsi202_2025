from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User
from .models import Student

@receiver(user_signed_up)
def create_student_on_signup(sender, request, user, **kwargs):
    # เช็คว่าผู้ใช้ใหม่ได้ถูกสร้างหรือไม่
    if user:
        # สร้างข้อมูลใน Student
        Student.objects.get_or_create(
            username="",
            email=user.email,
            birth="",  # สามารถเพิ่มค่าเริ่มต้นได้
            level="",
            grade="",
            degree="",
            interest=""
        )