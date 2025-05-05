from django.db import models
from django.core.exceptions import ValidationError

class Student(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    major = models.CharField(max_length=100)
    grade = models.CharField(max_length=50)
    hobby = models.TextField()
    interest = models.TextField(blank=True, null=True)



class Camp(models.Model):
    name = models.CharField(max_length=150)  # ชื่อผู้จัด
    email = models.EmailField()
    phone_num = models.CharField(max_length=20)
    camp_name = models.CharField(max_length=200)
    description_camp = models.TextField()
    upload_file = models.FileField(upload_to='camp_uploads/')
    CAMP_TYPE_CHOICES = [('health','ค่ายสายสุขภาพ'),('engineer','ค่ายสายวิศวกรรม'),('language','ค่ายสายภาษา'),('architecture','ค่ายสายสถาปัตย์'),('volunteer','ค่ายอาสา'),('digital_it','ค่ายสายดิจิทัล/IT'),('other','อื่นๆ'),]
    typeof_camp = models.CharField(max_length=20,choices=CAMP_TYPE_CHOICES,verbose_name='ประเภทค่าย')
    start_date = models.DateField()
    final_date = models.DateField()
    due_date = models.DateField()
    num_candi = models.PositiveIntegerField()

    PAYMENT_CHOICES = [('none', 'ไม่มีค่าใช้จ่าย'),('pre',  'จ่ายตอนสมัคร'),('post', 'จ่ายหลังประกาศรายชื่อ'),]
    payment_type = models.CharField(max_length=10,choices=PAYMENT_CHOICES,verbose_name='วิธีการชำระ')
    price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)

    candi_proper = models.TextField(blank=True, null=True)

    ACTIVITY_MODE_CHOICES = [('online', 'กิจกรรมออนไลน์'),('onsite', 'กิจกรรมออนไซต์'),]
    activity_mode = models.CharField(max_length=10, choices=ACTIVITY_MODE_CHOICES)
    place = models.CharField(max_length=200, blank=True, null=True)

    ig = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    line = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    linkcamp = models.URLField()
    organize_camp = models.CharField(max_length=200)
    has_organized = models.BooleanField(null=True,verbose_name='เคยจัดไหม',help_text='ติ๊กถ้าคุณเคยจัดค่ายนี้')
    detail_activity = models.TextField()
    poster = models.ImageField(upload_to='camp_posters/', blank=True, null=True)
    prove = models.BooleanField(default=False)


    def clean(self):
        super().clean()
        errors = {}

        # ——— ตรวจก่อนบันทึก ———
        # 1) ถ้าเลือก pre/post แต่ไม่กรอก price → error
        if self.payment_type in ('pre', 'post') and self.price is None:
            errors['price'] = 'กรุณาระบุจำนวนเงิน'
        # 2) ถ้าเลือก none → ล้าง price ออก
        if self.payment_type == 'none':
            self.price = None
        # 3) ถ้าเลือก onsite แต่ไม่กรอก place → error
        if self.activity_mode == 'onsite' and not self.place:
            errors['place'] = 'กรุณาระบุสถานที่จัดกิจกรรมออนไซต์'
        # 4) ถ้าเลือก online → ล้าง place ออก
        if self.activity_mode == 'online':
            self.place = None

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # รับประกันความสะอาดของข้อมูลทุกครั้งก่อนบันทึก
        if self.payment_type == 'none':
            self.price = None
        if self.activity_mode == 'online':
            self.place = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.camp_name