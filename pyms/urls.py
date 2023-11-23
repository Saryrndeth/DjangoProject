from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'pyms'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/<str:pri>', views.index, name='index_pri'),
    path('question/detail/<int:question_id>', views.question_detail, name='question_detail'),
    path('question/write', views.question_write, name='question_write'),
    path('answer/write/<int:question_id>', views.answer_write, name='answer_write'),
    path('ajax_menu/', views.ajax_request_menu, name='ajax_menu'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/vote/<int:question_id>/', views.question_vote, name='question_vote'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
    path('answer/vote/<int:answer_id>/', views.answer_vote, name='answer_vote'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)