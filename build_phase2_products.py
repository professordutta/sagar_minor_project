import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

base_dir = "d:/sagar_minor_project/crm_project"

# ----------------- PRODUCTS -----------------

products_views = """from django.urls import reverse_lazy
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
"""

products_urls = """from django.urls import path
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
"""

products_forms = """from django import forms
from .models import Product, SerialNumber

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'sku', 'name', 'brand', 'category', 'model_number', 'description',
            'mrp', 'selling_price', 'tax_percent', 'warranty_period', 
            'warranty_type', 'requires_serial_tracking', 'status'
        ]

class SerialNumberForm(forms.ModelForm):
    class Meta:
        model = SerialNumber
        fields = [
            'product', 'serial_number', 'customer', 'purchase_date',
            'warranty_start', 'warranty_end', 'status'
        ]
"""

products_list_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Products</h1>
    <div>
        <a href="{% url 'products:serial_list' %}" class="bg-indigo-600 text-white px-4 py-2 rounded shadow hover:bg-indigo-700 mr-2">Manage Serial Numbers</a>
        <a href="{% url 'products:create' %}" class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700">Add Product</a>
    </div>
</div>
<div class="bg-white shadow rounded-lg overflow-hidden">
    <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">SKU</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Brand</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Price</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            {% for product in products %}
            <tr>
                <td class="px-6 py-4 whitespace-nowrap">{{ product.sku }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ product.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ product.brand.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap">₹{{ product.selling_price }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ product.get_status_display }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <a href="{% url 'products:update' product.pk %}" class="text-indigo-600 hover:text-indigo-900 mr-3">Edit</a>
                    <a href="{% url 'products:detail' product.pk %}" class="text-blue-600 hover:text-blue-900">View</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="6" class="px-6 py-4 text-center text-gray-500">No products found.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
"""

products_form_html = """{% extends 'dashboard/base.html' %}
{% load crispy_forms_tags %}
{% block content %}
<div class="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow">
    <h1 class="text-2xl font-bold mb-6">{% if object %}Edit Product{% else %}Add Product{% endif %}</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <div class="grid grid-cols-2 gap-4">
            {{ form|crispy }}
        </div>
        <div class="mt-6 flex justify-end gap-4">
            <a href="{% url 'products:list' %}" class="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300">Cancel</a>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Save</button>
        </div>
    </form>
</div>
{% endblock %}
"""

products_detail_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="bg-white shadow rounded-lg p-6">
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">{{ product.name }}</h1>
        <a href="{% url 'products:update' product.pk %}" class="bg-indigo-600 text-white px-4 py-2 rounded shadow hover:bg-indigo-700">Edit</a>
    </div>
    <div class="grid grid-cols-2 gap-4">
        <div><strong>SKU:</strong> {{ product.sku }}</div>
        <div><strong>Brand:</strong> {{ product.brand.name }}</div>
        <div><strong>Category:</strong> {{ product.category.name }}</div>
        <div><strong>Model Number:</strong> {{ product.model_number }}</div>
        <div><strong>MRP:</strong> ₹{{ product.mrp }}</div>
        <div><strong>Selling Price:</strong> ₹{{ product.selling_price }}</div>
        <div><strong>Warranty:</strong> {{ product.warranty_period }} months ({{ product.get_warranty_type_display }})</div>
        <div><strong>Status:</strong> {{ product.get_status_display }}</div>
        <div class="col-span-2"><strong>Description:</strong> <p>{{ product.description }}</p></div>
    </div>
</div>
{% endblock %}
"""

serial_list_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Serial Numbers</h1>
    <div>
        <a href="{% url 'products:list' %}" class="bg-gray-600 text-white px-4 py-2 rounded shadow hover:bg-gray-700 mr-2">Back to Products</a>
        <a href="{% url 'products:serial_create' %}" class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700">Add Serial Number</a>
    </div>
</div>
<div class="bg-white shadow rounded-lg overflow-hidden">
    <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Product</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Serial Number</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Customer</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            {% for serial in serials %}
            <tr>
                <td class="px-6 py-4 whitespace-nowrap">{{ serial.product.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ serial.serial_number }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ serial.customer|default:"-" }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ serial.get_status_display }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <a href="{% url 'products:serial_update' serial.pk %}" class="text-indigo-600 hover:text-indigo-900">Edit</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">No serial numbers found.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
"""

serial_form_html = """{% extends 'dashboard/base.html' %}
{% load crispy_forms_tags %}
{% block content %}
<div class="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow">
    <h1 class="text-2xl font-bold mb-6">{% if object %}Edit Serial Number{% else %}Add Serial Number{% endif %}</h1>
    <form method="post">
        {% csrf_token %}
        {{ form|crispy }}
        <div class="mt-6 flex justify-end gap-4">
            <a href="{% url 'products:serial_list' %}" class="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300">Cancel</a>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Save</button>
        </div>
    </form>
</div>
{% endblock %}
"""

write_file(f"{base_dir}/products/views.py", products_views)
write_file(f"{base_dir}/products/urls.py", products_urls)
write_file(f"{base_dir}/products/forms.py", products_forms)
write_file(f"{base_dir}/templates/products/product_list.html", products_list_html)
write_file(f"{base_dir}/templates/products/product_form.html", products_form_html)
write_file(f"{base_dir}/templates/products/product_detail.html", products_detail_html)
write_file(f"{base_dir}/templates/products/serial_list.html", serial_list_html)
write_file(f"{base_dir}/templates/products/serial_form.html", serial_form_html)

print("Products module generated.")

