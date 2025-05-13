from django import forms
from .models import Camp

class CampForm(forms.ModelForm):
    class Meta:
        model = Camp
        fields = [
            'name', 'email', 'phone_num', 'camp_name', 'description_camp', 'upload_file', 
            'typeof_camp', 'start_date', 'end_date', 'final_date', 'num_candi', 'payment_type', 
            'price', 'primary', 'primary_grade_condition', 'primary_grade_from', 'primary_grade_to', 
            'secondary', 'secondary_grade_condition', 'secondary_grade_from', 'secondary_grade_to', 
            'vocational_minor', 'vocational_major', 'drop', 'degree', 'degree_grade_condition', 
            'degree_from', 'degree_to', 'other', 'age_condition', 'min_age', 'activity_mode', 'place', 
            'ig', 'facebook', 'line', 'website', 'linkcamp', 'organize_camp', 'has_organized', 
            'detail_activity', 'poster'
        ]


from .models import Student

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['username', 'birth', 'level', 'grade', 'degree', 'interest', 'profile_picture']
        
    birth = forms.DateField(
        widget=forms.DateInput(format='%m/%d/%Y')  # กำหนดรูปแบบวันที่
    )

    def clean(self):
        cleaned_data = super().clean()
        level = cleaned_data.get('level')
        grade = cleaned_data.get('grade')
        degree = cleaned_data.get('degree')

        if level in ['primary', 'secondary'] and not grade:
            self.add_error('grade', 'กรุณากรอกเกรด (1-6 สำหรับประถม/มัธยม)')
        
        if level == 'degree' and not degree:
            self.add_error('degree', 'กรุณาเลือกระดับปริญญา (ตรี, โท, เอก)')
        
        if level in ['vocational_minor', 'vocational_major', 'drop', 'other']:
            cleaned_data['grade'] = None
            cleaned_data['degree'] = None

        return cleaned_data