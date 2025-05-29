from django.contrib import admin
from .models import Student, Camp


# การแสดงข้อมูลของ Student
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'birth', 'level', 'grade', 'degree', 'interest', 'profile_picture')
    list_filter = ('level', 'degree')  
    search_fields = ('username', 'email')  
    ordering = ('username',)  

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'birth')
        }),
        ('ระดับการศึกษา', {
            'fields': ('level', 'grade', 'degree')
        }),
        ('ความสนใจ', {
            'fields': ('interest',)
        }),
        ('รูปโปรไฟล์', {
            'fields': ('profile_picture',)
        }),
    )


class CampAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'camp_name', 'typeof_camp', 'start_date', 'end_date', 'num_candi', 
        'payment_type', 'price', 'primary', 'secondary', 'vocational_minor', 'vocational_major',
        'drop', 'degree', 'age_condition', 'min_age', 'activity_mode', 'place', 'organize_camp', 
        'has_organized', 'poster', 'prove'
    )
    list_filter = (
        'typeof_camp', 'payment_type', 'primary', 'secondary', 'vocational_minor', 
        'vocational_major', 'drop', 'degree', 'age_condition', 'activity_mode'
    )
    search_fields = ('name', 'camp_name', 'organize_camp', 'detail_activity')
    ordering = ('-start_date',)
    list_editable = ('price', 'num_candi', 'has_organized')

    # กำหนดการแสดงผลของฟอร์มในหน้า edit 
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone_num', 'camp_name', 'description_camp', 'upload_file', 'typeof_camp', 'start_date', 'end_date', 'final_date', 'num_candi')
        }),
        ('Payment Information', {
            'fields': ('payment_type', 'price',)
        }),
        ('Education Information', {
            'fields': ('primary', 'primary_grade_condition', 'primary_grade_from', 'primary_grade_to', 
                       'secondary', 'secondary_grade_condition', 'secondary_grade_from', 'secondary_grade_to', 
                       'vocational_minor', 'vocational_major', 'drop', 'degree', 'degree_grade_condition', 'degree_from', 
                       'degree_to', 'other')
        }),
        ('Age Information', {
            'fields': ('age_condition', 'min_age')
        }),
        ('Activity Information', {
            'fields': ('activity_mode', 'place', 'detail_activity', 'linkcamp', 'organize_camp', 'has_organized')
        }),
        ('Social Media', {
            'fields': ('ig', 'facebook', 'line', 'website')
        }),
        ('Images', {
            'fields': ('poster', 'prove')
        }),
    )

# ลงทะเบียน Model กับ Admin
admin.site.register(Student, StudentAdmin)
admin.site.register(Camp, CampAdmin)
