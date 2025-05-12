
from django.db import models
from django.core.exceptions import ValidationError


class Student(models.Model):
    LEVEL_CHOICES = [
        ('primary', 'ประถม'),
        ('secondary', 'มัธยม'),
        ('vocational_minor', 'ปวช'),
        ('vocational_major', 'ปวส'),
        ('drop', 'เด็กซิ่ว'),
        ('degree', 'ปริญญา'),
        ('other', 'บุคคลทั่วไป'),
    ]
    
    GRADE_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    ]
    
    DEGREE_CHOICES = [
        ('bachelor', 'ตรี'),
        ('master', 'โท'),
        ('doctorate', 'เอก'),
    ]

    username = models.CharField(max_length=150)
    email = models.EmailField()
    birth = models.DateField(blank=True, null=True)  # วันเกิด
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, blank=True, null=True)  # ระดับการศึกษา
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True, null=True)  # เกรด (1-6)
    degree = models.CharField(max_length=20, blank=True, null=True, choices=DEGREE_CHOICES)  # ระดับปริญญา
    interest = models.TextField(blank=True, null=True)
    

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


    name = models.CharField(max_length=150)  # ชื่อผู้จัด
    email = models.EmailField()
    phone_num = models.CharField(max_length=20)
    camp_name = models.CharField(max_length=200)
    description_camp = models.TextField()
    upload_file = models.FileField(upload_to='camp_uploads/')
    CAMP_TYPE_CHOICES = [('health','ค่ายสายสุขภาพ'),('engineer','ค่ายสายวิศวกรรม'),('language','ค่ายสายภาษา'),('architecture','ค่ายสายสถาปัตย์'),('volunteer','ค่ายอาสา'),('digital_it','ค่ายสายดิจิทัล/IT'),('other','อื่นๆ'),]
    typeof_camp = models.CharField(max_length=20,choices=CAMP_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    final_date = models.DateField()
    num_candi = models.PositiveIntegerField()

    PAYMENT_CHOICES = [('none', 'ไม่มีค่าใช้จ่าย'),('pre',  'จ่ายตอนสมัคร'),('post', 'จ่ายหลังประกาศรายชื่อ'),]
    payment_type = models.CharField(max_length=10,choices=PAYMENT_CHOICES,verbose_name='วิธีการชำระ')
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
    linkcamp = models.URLField()
    organize_camp = models.CharField(max_length=200)
    has_organized = models.BooleanField()
    detail_activity = models.TextField()
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
            if self.primary_grade_from < 1 or self.primary_grade_from > 6:
                raise ValidationError('กรอกเกรดจากต้องอยู่ระหว่าง 1-6')
            if self.primary_grade_to < 1 or self.primary_grade_to > 6:
                raise ValidationError('กรอกเกรดถึงต้องอยู่ระหว่าง 1-6')
            if self.primary_grade_from > self.primary_grade_to:
                raise ValidationError('เกรดจากต้องน้อยกว่าเกรดถึง')

        if self.secondary and self.secondary_grade_condition == 'from':
            if not self.secondary_grade_from or not self.secondary_grade_to:
                raise ValidationError('กรุณากรอกเกรดจากและเกรดถึงสำหรับมัธยม')
            if self.secondary_grade_from < 1 or self.secondary_grade_from > 6:
                raise ValidationError('กรอกเกรดจากต้องอยู่ระหว่าง 1-6')
            if self.secondary_grade_to < 1 or self.secondary_grade_to > 6:
                raise ValidationError('กรอกเกรดถึงต้องอยู่ระหว่าง 1-6')
            if self.secondary_grade_from > self.secondary_grade_to:
                raise ValidationError('เกรดจากต้องน้อยกว่าเกรดถึง')

        if self.degree and self.degree_grade_condition == 'from':
            if not self.degree_from or not self.degree_to:
                raise ValidationError('กรุณากรอกระดับปริญญาจากและถึง')
            if self.degree_from not in ['bachelor', 'doctorate']:
                raise ValidationError('กรอกระดับปริญญาจากต้องเป็น ตรี หรือ เอก')
            if self.degree_to not in ['bachelor', 'doctorate']:
                raise ValidationError('กรอกระดับปริญญาถึงต้องเป็น ตรี หรือ เอก')
            if self.degree_from > self.degree_to:
                raise ValidationError('ระดับปริญญาจากต้องน้อยกว่าหรือเท่ากับระดับปริญญาถึง')

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # รับประกันความสะอาดของข้อมูลทุกครั้งก่อนบันทึก
        if self.payment_type == 'none':
            self.price = None
        if self.activity_mode == 'online':
            self.place = None
        if self.level == 'primary' or self.level == 'secondary':
            self.level_info = {self.level: [self.grade_from, self.grade_to]}
        elif self.level == 'degree':
            self.level_info = {'degree': [self.degree_from, self.degree_to]}
        else:
            self.level_info = {self.level: []}
        super().save(*args, **kwargs)

    def __str__(self):
        return self.camp_name