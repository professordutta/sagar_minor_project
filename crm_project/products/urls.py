from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('add/', views.ProductCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ProductUpdateView.as_view(), name='update'),
    path('serials/', views.SerialNumberListView.as_view(), name='serial_list'),
    path('serials/add/', views.SerialNumberCreateView.as_view(), name='serial_create'),
    path('serials/<int:pk>/edit/', views.SerialNumberUpdateView.as_view(), name='serial_update'),
]
