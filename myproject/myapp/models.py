
from django.db import models
from django.core.exceptions import ValidationError



class Student(models.Model):
    email = models.EmailField()  # ใช้ email เป็นตัวระบุหลัก
    username = models.CharField(max_length=150,blank=True)  # ชื่อผู้ใช้
    birth = models.DateField(blank=True, null=True)  # วันเกิด
    level = models.CharField(max_length=20, choices=[
        ('primary', 'ประถม'),
        ('secondary', 'มัธยม'),
        ('vocational_minor', 'ปวช'),
        ('vocational_major', 'ปวส'),
        ('drop', 'เด็กซิ่ว'),
        ('degree', 'ปริญญา'),
        ('other', 'บุคคลทั่วไป'),
    ], blank=True, null=True)  # ระดับการศึกษา
    grade = models.CharField(max_length=1, choices=[
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    ], blank=True, null=True)  # เกรด (1-6)
    degree = models.CharField(max_length=20, choices=[
        ('bachelor', 'ตรี'),
        ('master', 'โท'),
        ('doctorate', 'เอก'),
    ], blank=True, null=True)  # ระดับปริญญา
    interest = models.TextField(blank=True, null=True)  # ความสนใจ
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # รูปโปรไฟล์

    def clean(self):
        super().clean()
        errors = {}

        # 1) หากเลือกประถม/มัธยม ต้องกรอกเกรด
        if self.level in ['primary', 'secondary'] and not self.grade:
            errors['grade'] = 'กรุณากรอกเกรด (1-6 สำหรับประถม/มัธยม)'

        # 2) หากเลือกปริญญา ต้องเลือก degree (ตรี, โท, เอก)
        if self.level == 'degree' and not self.degree:
            errors['degree'] = 'กรุณาเลือกระดับปริญญา (ตรี, โท, เอก)'

        # 3) หากเลือกปวช/ปวส หรือ บุคคลทั่วไป ไม่มีความจำเป็นต้องกรอกเกรดหรือ degree
        if self.level in ['vocational_minor', 'vocational_major', 'drop', 'other']:
            self.grade = None
            self.degree = None

        if self.interest:
            interest_list = self.interest.split(',')
            if len(interest_list) > 5:
                raise ValidationError({'interest': 'กรุณากรอกความสนใจไม่เกิน 5 รายการ'})
            
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.username




class Camp(models.Model):


    name = models.CharField(max_length=150,null=True)  # ชื่อผู้จัด
    email = models.EmailField(unique=True)
    phone_num = models.CharField(max_length=20,null=True,blank=True)
    camp_name = models.CharField(max_length=200, null=True)
    description_camp = models.TextField(null=True)
    upload_file = models.FileField(upload_to='camp_uploads/',null=True)
    CAMP_TYPE_CHOICES = [('health','ค่ายสายสุขภาพ'),('engineer','ค่ายสายวิศวกรรม'),('language','ค่ายสายภาษา'),('architecture','ค่ายสายสถาปัตย์'),('volunteer','ค่ายอาสา'),('digital_it','ค่ายสายดิจิทัล/IT'),('other','อื่นๆ'),]
    typeof_camp = models.CharField(max_length=20,choices=CAMP_TYPE_CHOICES,null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    final_date = models.DateField(null=True)
    num_candi = models.PositiveIntegerField(null=True)

    PAYMENT_CHOICES = [('none', 'ไม่มีค่าใช้จ่าย'),('pre',  'จ่ายตอนสมัคร'),('post', 'จ่ายหลังประกาศรายชื่อ'),]
    payment_type = models.CharField(max_length=10,choices=PAYMENT_CHOICES,verbose_name='วิธีการชำระ',null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    # สำหรับเลือกระดับการศึกษา
    primary = models.BooleanField(default=False)
    primary_grade_condition = models.CharField(
        max_length=20, choices=[('all', 'ทั้งหมด'), ('from', 'ตั้งแต่')],
        blank=True, null=True
    )
    primary_grade_from = models.IntegerField(blank=True, null=True)
    primary_grade_to = models.IntegerField(blank=True, null=True)

    secondary = models.BooleanField(default=False)
    secondary_grade_condition = models.CharField(
        max_length=20, choices=[('all', 'ทั้งหมด'), ('from', 'ตั้งแต่')],
        blank=True, null=True
    )
    secondary_grade_from = models.IntegerField(blank=True, null=True)
    secondary_grade_to = models.IntegerField(blank=True, null=True)

    vocational_minor = models.BooleanField(default=False)
    vocational_major = models.BooleanField(default=False)
    drop = models.BooleanField(default=False)
    degree = models.BooleanField(default=False)
    degree_grade_condition = models.CharField(
        max_length=20, choices=[('all', 'ทั้งหมด'), ('from', 'ตั้งแต่')],
        blank=True, null=True
    )
    degree_from = models.CharField(
        max_length=20, choices=[('bachelor', 'ตรี'), ('master', 'โท'), ('doctorate', 'เอก')],
        blank=True, null=True
    )
    degree_to = models.CharField(
        max_length=20, choices=[('bachelor', 'ตรี'), ('master', 'โท'), ('doctorate', 'เอก')],
        blank=True, null=True)

    other = models.BooleanField(default=False) #บุคคลทั่วไป


    AGE_CHOICES = [
        ('no_limit', 'ไม่กำหนด'),
        ('from', 'ตั้งแต่'),
    ]

 
    age_condition = models.CharField(max_length=20, choices=AGE_CHOICES, blank=True, null=True)
    min_age = models.IntegerField(blank=True, null=True)  # อายุขั้นต่ำหากเลือก "ตั้งแต่"




    ACTIVITY_MODE_CHOICES = [('online', 'กิจกรรมออนไลน์'),('onsite', 'กิจกรรมออนไซต์'),]
    activity_mode = models.CharField(max_length=10, choices=ACTIVITY_MODE_CHOICES)
    place = models.CharField(max_length=200, blank=True, null=True)

    ig = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    line = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    linkcamp = models.URLField(null=True)
    organize_camp = models.CharField(max_length=200, blank=True, null=True)
    has_organized = models.BooleanField( blank=True,default=False)
    detail_activity = models.TextField(null=True)
    poster = models.ImageField(upload_to='camp_posters/', blank=True, null=True)
    prove = models.BooleanField(default=False)


    def clean(self):
        super().clean()
        errors = {}

        # ตรวจสอบการกรอกข้อมูลเกี่ยวกับการชำระเงิน
        if self.payment_type in ('pre', 'post') and self.price is None:
            errors['price'] = 'กรุณาระบุจำนวนเงิน'
        if self.payment_type == 'none':
            self.price = None

        # ตรวจสอบการกรอกข้อมูลเกี่ยวกับสถานที่
        if self.activity_mode == 'onsite' and not self.place:
            errors['place'] = 'กรุณาระบุสถานที่จัดกิจกรรมออนไซต์'
        if self.activity_mode == 'online':
            self.place = None

            
        if self.age_condition == 'no_limit':
            self.min_age = 0


        if self.primary and self.primary_grade_condition == 'all':
            self.primary_grade_from = 1
            self.primary_grade_to = 6

        if self.secondary and self.secondary_grade_condition == 'all':
            self.secondary_grade_from = 1
            self.secondary_grade_to = 6

        if self.degree and self.degree_grade_condition == 'all':
            self.degree_from = 'bachelor'  # ค่าเริ่มต้นสำหรับ degree
            self.degree_to = 'doctorate'   # ค่าเริ่มต้นสำหรับ degree

        # ตรวจสอบกรณี "ตั้งแต่" ที่จะต้องกรอกค่า
        if self.primary and self.primary_grade_condition == 'from':
            if not self.primary_grade_from or not self.primary_grade_to:
                raise ValidationError('กรุณากรอกเกรดจากและเกรดถึงสำหรับประถม')
            if self.primary_grade_from < 0 or self.primary_grade_from > 6:
                raise ValidationError('กรอกเกรดจากต้องอยู่ระหว่าง 1-6')
            if self.primary_grade_to < 0 or self.primary_grade_to > 6:
                raise ValidationError('กรอกเกรดถึงต้องอยู่ระหว่าง 1-6')
            if self.primary_grade_from > self.primary_grade_to:
                raise ValidationError('เกรดจากต้องน้อยกว่าเกรดถึง')

        if self.secondary and self.secondary_grade_condition == 'from':
            if not self.secondary_grade_from or not self.secondary_grade_to:
                raise ValidationError('กรุณากรอกเกรดจากและเกรดถึงสำหรับมัธยม')
            if self.secondary_grade_from < 0 or self.secondary_grade_from > 6:
                raise ValidationError('กรอกเกรดจากต้องอยู่ระหว่าง 1-6')
            if self.secondary_grade_to < 0 or self.secondary_grade_to > 6:
                raise ValidationError('กรอกเกรดถึงต้องอยู่ระหว่าง 1-6')
            if self.secondary_grade_from > self.secondary_grade_to:
                raise ValidationError('เกรดจากต้องน้อยกว่าเกรดถึง')

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