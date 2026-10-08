from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('', views.ServiceListView.as_view(), name='list'),
    path('add/', views.ServiceCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ServiceDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='update'),
]
