from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('service-agent/', views.service_agent_dashboard, name='service_agent_dashboard'),
    path('sales/', views.sales_dashboard, name='sales_dashboard'),
    path('technician/', views.technician_dashboard, name='technician_dashboard'),
]
