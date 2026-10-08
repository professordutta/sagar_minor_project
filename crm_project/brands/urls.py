from django.urls import path
from . import views

app_name = 'brands'

urlpatterns = [
    path('', views.BrandListView.as_view(), name='list'),
    path('add/', views.BrandCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BrandDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.BrandUpdateView.as_view(), name='update'),
]
