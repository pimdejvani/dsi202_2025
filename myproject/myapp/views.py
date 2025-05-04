# myproject/myapp/views.py

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # แบบง่าย: ส่งข้อความ
    return HttpResponse("Hello from myapp index!")