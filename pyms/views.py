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
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request, pri=''):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')  # 검색어
    private = request.GET.get('pri', '')
    print(pri)
    if pri:
        private = pri
    if private:
        question_list = Question.objects.filter(private=private).order_by('-create_date')
    else:
        question_list = Question.objects.filter(private="전체").order_by('-create_date')
        private = "전체"
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) | # 답변 내용 검색
            # 게시글의 학교 검색
            Q(School__icontains=kw)
        ).distinct()
    paginator = Paginator(question_list, 10)

    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'private': private}
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
            question.imgfile = request.FILES.get('imgfile')
            question.create_date = timezone.now()
            question.save()
            if request.POST.get('private') == '학교':
                return redirect('pyms:index_pri', pri=request.user.School)
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


@login_required(login_url='login:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.user:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pyms:question_detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pyms:question_detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pyms/question_form.html', context)


@login_required(login_url='login:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.user:
        print(1)
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('pyms:question_detail', question_id=question.id)


@login_required(login_url='login:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.user:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pyms:question_detail', question_id=question.id)
    question.delete()
    return redirect('pyms:index')


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.user:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pyms:question_detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pyms:question_detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pyms/answer_form.html', context)


@login_required(login_url='login:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.user:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pyms:question_detail', question_id=answer.question.id)


@login_required(login_url='login:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.user:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('pyms:question_detail', question_id=answer.question.id)
