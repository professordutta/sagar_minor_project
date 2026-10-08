import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

base_dir = "d:/sagar_minor_project/crm_project"

# ----------------- BRANDS -----------------

brands_views = """from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Brand
from .forms import BrandForm

class BrandListView(LoginRequiredMixin, ListView):
    model = Brand
    template_name = 'brands/brand_list.html'
    context_object_name = 'brands'

class BrandCreateView(LoginRequiredMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'brands/brand_form.html'
    success_url = reverse_lazy('brands:list')

class BrandUpdateView(LoginRequiredMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'brands/brand_form.html'
    success_url = reverse_lazy('brands:list')

class BrandDetailView(LoginRequiredMixin, DetailView):
    model = Brand
    template_name = 'brands/brand_detail.html'
    context_object_name = 'brand'
"""

brands_urls = """from django.urls import path
from . import views

app_name = 'brands'

urlpatterns = [
    path('', views.BrandListView.as_view(), name='list'),
    path('add/', views.BrandCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BrandDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.BrandUpdateView.as_view(), name='update'),
]
"""

brands_forms = """from django import forms
from .models import Brand

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'slug', 'description', 'website', 'status', 'is_active']
"""

brands_list_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Brands</h1>
    <a href="{% url 'brands:create' %}" class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700">Add Brand</a>
</div>
<div class="bg-white shadow rounded-lg overflow-hidden">
    <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            {% for brand in brands %}
            <tr>
                <td class="px-6 py-4 whitespace-nowrap">{{ brand.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ brand.get_status_display }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <a href="{% url 'brands:update' brand.pk %}" class="text-indigo-600 hover:text-indigo-900 mr-3">Edit</a>
                    <a href="{% url 'brands:detail' brand.pk %}" class="text-blue-600 hover:text-blue-900">View</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="3" class="px-6 py-4 text-center text-gray-500">No brands found.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
"""

brands_form_html = """{% extends 'dashboard/base.html' %}
{% load crispy_forms_tags %}
{% block content %}
<div class="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow">
    <h1 class="text-2xl font-bold mb-6">{% if object %}Edit Brand{% else %}Add Brand{% endif %}</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form|crispy }}
        <div class="mt-6 flex justify-end gap-4">
            <a href="{% url 'brands:list' %}" class="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300">Cancel</a>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Save</button>
        </div>
    </form>
</div>
{% endblock %}
"""

brands_detail_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="bg-white shadow rounded-lg p-6">
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">{{ brand.name }}</h1>
        <a href="{% url 'brands:update' brand.pk %}" class="bg-indigo-600 text-white px-4 py-2 rounded shadow hover:bg-indigo-700">Edit</a>
    </div>
    <div class="grid grid-cols-2 gap-4">
        <div><strong>Status:</strong> {{ brand.get_status_display }}</div>
        <div><strong>Website:</strong> {{ brand.website }}</div>
        <div class="col-span-2"><strong>Description:</strong> <p>{{ brand.description }}</p></div>
    </div>
</div>
{% endblock %}
"""

write_file(f"{base_dir}/brands/views.py", brands_views)
write_file(f"{base_dir}/brands/urls.py", brands_urls)
write_file(f"{base_dir}/brands/forms.py", brands_forms)
write_file(f"{base_dir}/templates/brands/brand_list.html", brands_list_html)
write_file(f"{base_dir}/templates/brands/brand_form.html", brands_form_html)
write_file(f"{base_dir}/templates/brands/brand_detail.html", brands_detail_html)

print("Brands module generated.")

