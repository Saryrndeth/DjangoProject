from django import forms
from pyms.models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['private', 'subject', 'content']
        labels = {
            'private': '게시판',
            'subject': '제목',
            'content': '내용',
        }
        widgets = {
            # 전체 게시판과 유저의 게시판을 선택 옵션으로 가지도록
            'private': forms.Select(attrs={'class': 'form-control'}, choices=(('전체', '전체'), ('학교', '학교'))),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '내용',
        }