from django.urls import path
from . import views

app_name = 'pyms'

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax_menu/', views.ajax_request_menu, name='ajax_menu')
]