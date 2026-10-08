from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, SerialNumber
from .forms import ProductForm, SerialNumberForm

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(is_deleted=False).select_related('brand', 'category')

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:list')

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:list')

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

class SerialNumberListView(LoginRequiredMixin, ListView):
    model = SerialNumber
    template_name = 'products/serial_list.html'
    context_object_name = 'serials'
    queryset = SerialNumber.objects.select_related('product', 'customer')

class SerialNumberCreateView(LoginRequiredMixin, CreateView):
    model = SerialNumber
    form_class = SerialNumberForm
    template_name = 'products/serial_form.html'
    success_url = reverse_lazy('products:serial_list')

class SerialNumberUpdateView(LoginRequiredMixin, UpdateView):
    model = SerialNumber
    form_class = SerialNumberForm
    template_name = 'products/serial_form.html'
    success_url = reverse_lazy('products:serial_list')
