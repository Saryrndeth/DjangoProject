from django import forms
from django.contrib.auth.forms import UserCreationForm
from pyms.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("nickname", "username", "password1", "password2", "email", "School", "Grade", "Class", "Number", "is_teacher")