from datetime import datetime
from comcigan import School
from .models import RegisteredSchool
from .func import *
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request, 'pyms/haksaeng_index.html')


def ajax_request_menu(request):
    if request.method == "POST":
        print(request.POST)
        school = request.POST['school']
        if school == '':
            return JsonResponse({'menu': ''
                , 'school': '로그인해주세요!', 'date': '', 'schedule': ''})
        try:
            schedule: list = School(shortschool(school))[int(request.POST['grade'])][int(request.POST['cls'])][datetime.today().weekday()]
            # shortschedule = lambda x: [i[0] for i in x]
            schedule = [i[0] for i in schedule]
        except Exception as e:
            print(e)
            schedule = getSchedule(school, request.POST['grade'], request.POST['cls'])
        return JsonResponse(({'menu': getGupsik(school)
            , 'school': school, 'date': timezone.now().strftime("%m월%d일"), 'schedule': schedule}))
