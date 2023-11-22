from datetime import datetime
from comcigan import School
from .models import RegisteredSchool
from .models import Question, Answer
from .func import *
from .forms import QuestionForm, AnswerForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse, HttpResponseNotAllowed
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')  # 검색어
    private = request.GET.get('pri', '')
    if private:
        question_list = Question.objects.filter(private=private).order_by('-create_date')
    else:
        question_list = Question.objects.filter(private="전체").order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) # 답변 내용 검색
        ).distinct()
    paginator = Paginator(question_list, 10)

    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'pyms/haksaeng_index.html', context)


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


def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pyms/question_detail.html', context)

def question_write(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            if request.POST.get('private') == '학교':
                question.private = request.user.School
            question.user = request.user
            question.nickname = request.user.nickname
            question.School = request.user.School
            question.is_teacher = request.user.is_teacher
            question.Grade = request.user.Grade
            question.create_date = timezone.now()
            question.save()
            return redirect('pyms:index')
    else:
        if request.user.is_anonymous:
            return HttpResponseNotAllowed("로그인이 필요합니다.")
        form = QuestionForm()
        return render(request, 'pyms/question_form.html', {'form': form})


def answer_write(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            print(question)
            question.answer_set.create(user=request.user, content=request.POST.get('content'), create_date=timezone.now(), nickname=request.user.nickname, School=request.user.School, is_teacher=request.user.is_teacher, Grade=request.user.Grade)
            return redirect('pyms:question_detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed("POST 요청이 아닙니다.")
    context = {'question': question, 'form': form}
    return render(request, 'pyms/question_detail.html', context)
