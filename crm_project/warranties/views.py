from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Warranty
from .forms import WarrantyForm


class WarrantyListView(LoginRequiredMixin, ListView):
    model = Warranty
    template_name = 'warranties/warranty_list.html'
    context_object_name = 'warranties'
    queryset = Warranty.objects.select_related('customer', 'product')


class WarrantyDetailView(LoginRequiredMixin, DetailView):
    model = Warranty
    template_name = 'warranties/warranty_detail.html'
    context_object_name = 'warranty'


class WarrantyCreateView(LoginRequiredMixin, CreateView):
    model = Warranty
    form_class = WarrantyForm
    template_name = 'warranties/warranty_form.html'
    success_url = reverse_lazy('warranties:list')


class WarrantyUpdateView(LoginRequiredMixin, UpdateView):
    model = Warranty
    form_class = WarrantyForm
    template_name = 'warranties/warranty_form.html'
    success_url = reverse_lazy('warranties:list')
