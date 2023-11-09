from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from login.forms import UserForm
from pyms.models import RegisteredSchool


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username').lower()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            sclist = RegisteredSchool.objects.all()
            sclist = [i.school for i in sclist]
            if form.cleaned_data.get('School') not in sclist:
                regschool = RegisteredSchool(school=form.cleaned_data.get('School'))
                regschool.save()

            return redirect('pyms:index')
    else:
        form = UserForm()
    return render(request, 'login/signup.html', {'form': form})