import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

base_dir = "d:/sagar_minor_project/crm_project"

# ----------------- CATEGORIES -----------------

categories_views = """from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category
from .forms import CategoryForm

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:list')

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:list')

class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'categories/category_detail.html'
    context_object_name = 'category'
"""

categories_urls = """from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='list'),
    path('add/', views.CategoryCreateView.as_view(), name='create'),
    path('<int:pk>/', views.CategoryDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='update'),
]
"""

categories_forms = """from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent', 'description', 'status']
"""

categories_list_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Categories</h1>
    <a href="{% url 'categories:create' %}" class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700">Add Category</a>
</div>
<div class="bg-white shadow rounded-lg overflow-hidden">
    <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Parent</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            {% for category in categories %}
            <tr>
                <td class="px-6 py-4 whitespace-nowrap">{{ category.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ category.parent.name|default:"-" }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ category.get_status_display }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <a href="{% url 'categories:update' category.pk %}" class="text-indigo-600 hover:text-indigo-900 mr-3">Edit</a>
                    <a href="{% url 'categories:detail' category.pk %}" class="text-blue-600 hover:text-blue-900">View</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4" class="px-6 py-4 text-center text-gray-500">No categories found.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
"""

categories_form_html = """{% extends 'dashboard/base.html' %}
{% load crispy_forms_tags %}
{% block content %}
<div class="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow">
    <h1 class="text-2xl font-bold mb-6">{% if object %}Edit Category{% else %}Add Category{% endif %}</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form|crispy }}
        <div class="mt-6 flex justify-end gap-4">
            <a href="{% url 'categories:list' %}" class="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300">Cancel</a>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Save</button>
        </div>
    </form>
</div>
{% endblock %}
"""

categories_detail_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="bg-white shadow rounded-lg p-6">
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">{{ category.name }}</h1>
        <a href="{% url 'categories:update' category.pk %}" class="bg-indigo-600 text-white px-4 py-2 rounded shadow hover:bg-indigo-700">Edit</a>
    </div>
    <div class="grid grid-cols-2 gap-4">
        <div><strong>Status:</strong> {{ category.get_status_display }}</div>
        <div><strong>Parent:</strong> {{ category.parent.name|default:"None" }}</div>
        <div class="col-span-2"><strong>Description:</strong> <p>{{ category.description }}</p></div>
    </div>
</div>
{% endblock %}
"""

write_file(f"{base_dir}/categories/views.py", categories_views)
write_file(f"{base_dir}/categories/urls.py", categories_urls)
write_file(f"{base_dir}/categories/forms.py", categories_forms)
write_file(f"{base_dir}/templates/categories/category_list.html", categories_list_html)
write_file(f"{base_dir}/templates/categories/category_form.html", categories_form_html)
write_file(f"{base_dir}/templates/categories/category_detail.html", categories_detail_html)

print("Categories module generated.")

