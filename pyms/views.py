import requests
from .func import *
from django.shortcuts import render
from django.utils import timezone


# Create your views here.
def index(request):
    print(getGupsik('선린인터넷고등학교'))
    return render(request, 'pyms/haksaeng_index.html', {'list': getGupsik('선린인터넷고등학교')
                                                            ,'school': '선린인터넷고등학교', 'date': timezone.now().strftime("%m월%d일")})
