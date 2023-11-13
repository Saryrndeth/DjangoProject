from django.urls import path
from . import views

app_name = 'pyms'

urlpatterns = [
    path('', views.index, name='index'),
    path('question/detail/<int:question_id>', views.question_detail, name='question_detail'),
    path('question/write', views.question_write, name='question_write'),
    path('answer/write/<int:question_id>', views.answer_write, name='answer_write'),
    path('ajax_menu/', views.ajax_request_menu, name='ajax_menu')
]