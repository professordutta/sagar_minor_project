import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

base_dir = "d:/sagar_minor_project/crm_project"

# ----------------- COMPLAINTS -----------------

complaints_views = """from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Complaint
from .forms import ComplaintForm

class ComplaintListView(LoginRequiredMixin, ListView):
    model = Complaint
    template_name = 'complaints/complaint_list.html'
    context_object_name = 'complaints'
    
    def get_queryset(self):
        return Complaint.objects.filter(is_deleted=False).select_related('customer', 'assigned_to')

class ComplaintCreateView(LoginRequiredMixin, CreateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = 'complaints/complaint_form.html'
    success_url = reverse_lazy('complaints:list')

class ComplaintUpdateView(LoginRequiredMixin, UpdateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = 'complaints/complaint_form.html'
    success_url = reverse_lazy('complaints:list')

class ComplaintDetailView(LoginRequiredMixin, DetailView):
    model = Complaint
    template_name = 'complaints/complaint_detail.html'
    context_object_name = 'complaint'
"""

complaints_urls = """from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    path('', views.ComplaintListView.as_view(), name='list'),
    path('add/', views.ComplaintCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ComplaintDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ComplaintUpdateView.as_view(), name='update'),
]
"""

complaints_forms = """from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['customer', 'order', 'product', 'serial_number', 'category', 'subject', 'description', 'priority', 'status', 'assigned_to']
"""

complaints_list_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Complaints & Tickets</h1>
    <a href="{% url 'complaints:create' %}" class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700">Add Complaint</a>
</div>
<div class="bg-white shadow rounded-lg overflow-hidden">
    <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ticket ID</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Customer</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Subject</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Priority</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Assigned To</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            {% for complaint in complaints %}
            <tr>
                <td class="px-6 py-4 whitespace-nowrap">{{ complaint.ticket_id }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ complaint.customer }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ complaint.subject }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ complaint.get_priority_display }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ complaint.get_status_display }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ complaint.assigned_to|default:"-" }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <a href="{% url 'complaints:update' complaint.pk %}" class="text-indigo-600 hover:text-indigo-900 mr-3">Edit</a>
                    <a href="{% url 'complaints:detail' complaint.pk %}" class="text-blue-600 hover:text-blue-900">View</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="7" class="px-6 py-4 text-center text-gray-500">No complaints found.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
"""

complaints_form_html = """{% extends 'dashboard/base.html' %}
{% load crispy_forms_tags %}
{% block content %}
<div class="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow">
    <h1 class="text-2xl font-bold mb-6">{% if object %}Edit Complaint{% else %}Add Complaint{% endif %}</h1>
    <form method="post">
        {% csrf_token %}
        <div class="grid grid-cols-2 gap-4">
            {{ form|crispy }}
        </div>
        <div class="mt-6 flex justify-end gap-4">
            <a href="{% url 'complaints:list' %}" class="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300">Cancel</a>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Save</button>
        </div>
    </form>
</div>
{% endblock %}
"""

complaints_detail_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="bg-white shadow rounded-lg p-6">
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">Ticket: {{ complaint.ticket_id }}</h1>
        <a href="{% url 'complaints:update' complaint.pk %}" class="bg-indigo-600 text-white px-4 py-2 rounded shadow hover:bg-indigo-700">Edit</a>
    </div>
    <div class="grid grid-cols-2 gap-4">
        <div><strong>Customer:</strong> {{ complaint.customer }}</div>
        <div><strong>Status:</strong> {{ complaint.get_status_display }}</div>
        <div><strong>Priority:</strong> {{ complaint.get_priority_display }}</div>
        <div><strong>Product:</strong> {{ complaint.product|default:"-" }}</div>
        <div><strong>Serial Number:</strong> {{ complaint.serial_number|default:"-" }}</div>
        <div><strong>Assigned To:</strong> {{ complaint.assigned_to|default:"Unassigned" }}</div>
        <div><strong>Created At:</strong> {{ complaint.created_at|date:"M d, Y H:i" }}</div>
        <div class="col-span-2"><strong>Subject:</strong> {{ complaint.subject }}</div>
        <div class="col-span-2"><strong>Description:</strong> <p class="mt-2">{{ complaint.description }}</p></div>
    </div>
</div>
{% endblock %}
"""

# ----------------- SERVICE -----------------

service_views = """from django.urls import reverse_lazy
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
"""

service_urls = """from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('', views.ServiceListView.as_view(), name='list'),
    path('add/', views.ServiceCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ServiceDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='update'),
]
"""

service_forms = """from django import forms
from .models import ServiceRequest

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['customer', 'complaint', 'product', 'serial_number', 'technician', 'status', 'description', 'scheduled_date']
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
"""

service_list_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Service Requests</h1>
    <a href="{% url 'service:create' %}" class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700">Add Service Request</a>
</div>
<div class="bg-white shadow rounded-lg overflow-hidden">
    <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Service ID</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Customer</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Technician</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Scheduled Date</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            {% for req in service_requests %}
            <tr>
                <td class="px-6 py-4 whitespace-nowrap">{{ req.service_id }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ req.customer }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ req.technician|default:"-" }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ req.get_status_display }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ req.scheduled_date|date:"M d, Y H:i"|default:"-" }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <a href="{% url 'service:update' req.pk %}" class="text-indigo-600 hover:text-indigo-900 mr-3">Edit</a>
                    <a href="{% url 'service:detail' req.pk %}" class="text-blue-600 hover:text-blue-900">View</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="6" class="px-6 py-4 text-center text-gray-500">No service requests found.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
"""

service_form_html = """{% extends 'dashboard/base.html' %}
{% load crispy_forms_tags %}
{% block content %}
<div class="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow">
    <h1 class="text-2xl font-bold mb-6">{% if object %}Edit Service Request{% else %}Add Service Request{% endif %}</h1>
    <form method="post">
        {% csrf_token %}
        <div class="grid grid-cols-2 gap-4">
            {{ form|crispy }}
        </div>
        <div class="mt-6 flex justify-end gap-4">
            <a href="{% url 'service:list' %}" class="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300">Cancel</a>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Save</button>
        </div>
    </form>
</div>
{% endblock %}
"""

service_detail_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="bg-white shadow rounded-lg p-6">
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">Service Request: {{ service_request.service_id }}</h1>
        <a href="{% url 'service:update' service_request.pk %}" class="bg-indigo-600 text-white px-4 py-2 rounded shadow hover:bg-indigo-700">Edit</a>
    </div>
    <div class="grid grid-cols-2 gap-4">
        <div><strong>Customer:</strong> {{ service_request.customer }}</div>
        <div><strong>Status:</strong> {{ service_request.get_status_display }}</div>
        <div><strong>Product:</strong> {{ service_request.product|default:"-" }}</div>
        <div><strong>Serial Number:</strong> {{ service_request.serial_number|default:"-" }}</div>
        <div><strong>Technician:</strong> {{ service_request.technician|default:"Unassigned" }}</div>
        <div><strong>Scheduled Date:</strong> {{ service_request.scheduled_date|date:"M d, Y H:i"|default:"-" }}</div>
        <div class="col-span-2"><strong>Description:</strong> <p class="mt-2">{{ service_request.description }}</p></div>
    </div>
</div>
{% endblock %}
"""

write_file(f"{base_dir}/complaints/views.py", complaints_views)
write_file(f"{base_dir}/complaints/urls.py", complaints_urls)
write_file(f"{base_dir}/complaints/forms.py", complaints_forms)
write_file(f"{base_dir}/templates/complaints/complaint_list.html", complaints_list_html)
write_file(f"{base_dir}/templates/complaints/complaint_form.html", complaints_form_html)
write_file(f"{base_dir}/templates/complaints/complaint_detail.html", complaints_detail_html)

write_file(f"{base_dir}/service/views.py", service_views)
write_file(f"{base_dir}/service/urls.py", service_urls)
write_file(f"{base_dir}/service/forms.py", service_forms)
write_file(f"{base_dir}/templates/service/service_list.html", service_list_html)
write_file(f"{base_dir}/templates/service/service_form.html", service_form_html)
write_file(f"{base_dir}/templates/service/service_detail.html", service_detail_html)

print("Complaints and Service modules generated.")

