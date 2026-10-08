from django.urls import path
from . import views

app_name = 'warranties'

urlpatterns = [
    path('', views.WarrantyListView.as_view(), name='list'),
    path('add/', views.WarrantyCreateView.as_view(), name='create'),
    path('<int:pk>/', views.WarrantyDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.WarrantyUpdateView.as_view(), name='update'),
]
