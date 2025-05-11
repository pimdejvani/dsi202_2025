from django.contrib import admin
from .models import Student, Camp

# ลงทะเบียนโมเดล Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'major', 'grade', 'hobby', 'interest')  # แสดงฟิลด์ในตาราง
    search_fields = ('username', 'email', 'major')  # ค้นหาจากฟิลด์เหล่านี้
    list_filter = ('major', 'grade')  # เพิ่มตัวกรองในหน้า admin

# ลงทะเบียนโมเดล Camp
@admin.register(Camp)
class CampAdmin(admin.ModelAdmin):
    list_display = ('camp_name', 'organize_camp', 'typeof_camp', 'start_date', 'final_date', 'payment_type', 'price', 'place', 'activity_mode', 'linkcamp', 'has_organized')  # แสดงฟิลด์ในตาราง
    search_fields = ('camp_name', 'organize_camp', 'typeof_camp')  # ค้นหาจากฟิลด์เหล่านี้
    list_filter = ('typeof_camp', 'payment_type', 'activity_mode')  # เพิ่มตัวกรองในหน้า admin
    date_hierarchy = 'start_date'  # เพิ่มการกรองตามวันที่ (สามารถคลิกเลือกวันที่)
    ordering = ('-start_date',)  # กำหนดให้เรียงจากวันที่เริ่มต้นล่าสุด

    # แสดงฟิลด์เพิ่มเติมเมื่อดูรายละเอียดค่าย (ในหน้า Detail view)
    fieldsets = (
        (None, {
            'fields': ('camp_name', 'organize_camp', 'description_camp', 'upload_file')
        }),
        ('ค่ายข้อมูลเพิ่มเติม', {
            'fields': ('typeof_camp', 'start_date', 'final_date', 'due_date', 'num_candi', 'payment_type', 'price', 'candi_proper', 'activity_mode', 'place')
        }),
        ('ช่องทางติดต่อ', {
            'fields': ('ig', 'facebook', 'line', 'website', 'linkcamp')
        }),
        ('รายละเอียดกิจกรรม', {
            'fields': ('detail_activity', 'poster', 'prove')
        }),
    )

    # เพิ่มฟิลด์ที่สามารถแก้ไขได้จากหน้า List view
    list_editable = ('price', 'has_organized')  # ทำให้ฟิลด์ราคาและสถานะจัดงานแก้ไขได้ในหน้า List view
