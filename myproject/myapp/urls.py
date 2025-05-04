# from django.urls import path
# from . import views

app_name = 'myapp'   # optional แต่ถ้าใช้ชื่อซ้ำกับแอปอื่น จะช่วยแยกเวลา reverse()

from django.urls import path
from .views import index

urlpatterns = [
    # '' หมายถึง path เปล่า (root ของ include)
    path('', index, name='index'),
]