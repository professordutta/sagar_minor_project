from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.feedback_list, name='list'),
    path('add/', views.feedback_create, name='create'),
]
