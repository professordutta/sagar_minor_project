from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    path('', views.ComplaintListView.as_view(), name='list'),
    path('add/', views.ComplaintCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ComplaintDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ComplaintUpdateView.as_view(), name='update'),
]
