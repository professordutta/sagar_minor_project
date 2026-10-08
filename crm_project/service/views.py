from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ServiceRequest
from .forms import ServiceRequestForm

class ServiceListView(LoginRequiredMixin, ListView):
    model = ServiceRequest
    template_name = 'service/service_list.html'
    context_object_name = 'service_requests'
    
    def get_queryset(self):
        return ServiceRequest.objects.select_related('customer', 'technician')

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = ServiceRequest
    form_class = ServiceRequestForm
    template_name = 'service/service_form.html'
    success_url = reverse_lazy('service:list')

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = ServiceRequest
    form_class = ServiceRequestForm
    template_name = 'service/service_form.html'
    success_url = reverse_lazy('service:list')

class ServiceDetailView(LoginRequiredMixin, DetailView):
    model = ServiceRequest
    template_name = 'service/service_detail.html'
    context_object_name = 'service_request'
