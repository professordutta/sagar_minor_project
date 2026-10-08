import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

base_dir = "d:/sagar_minor_project/crm_project"

# ----------------- CUSTOMERS -----------------

customers_views = """from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer
from .forms import CustomerForm
from orders.models import Order
from warranties.models import Warranty
from complaints.models import Complaint
from service.models import ServiceRequest

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'
    queryset = Customer.objects.filter(is_deleted=False)

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers:list')

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers:list')

class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.object
        context['orders'] = Order.objects.filter(customer=customer)
        context['warranties'] = Warranty.objects.filter(customer=customer)
        context['complaints'] = Complaint.objects.filter(customer=customer)
        context['service_requests'] = ServiceRequest.objects.filter(customer=customer)
        context['total_spent'] = sum(order.grand_total for order in context['orders'] if order.payment_status == 'paid')
        return context
"""

customers_urls = """from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.CustomerListView.as_view(), name='list'),
    path('add/', views.CustomerCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.CustomerDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', views.CustomerUpdateView.as_view(), name='update'),
]
"""

customers_forms = """from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'first_name', 'last_name', 'email', 'mobile', 'alternate_mobile',
            'date_of_birth', 'gender', 'address', 'city', 'state', 'pin_code',
            'country', 'customer_type', 'preferred_contact', 'account_status', 'notes'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
"""

customers_list_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Customers</h1>
    <a href="{% url 'customers:create' %}" class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700">Add Customer</a>
</div>
<div class="bg-white shadow rounded-lg overflow-hidden">
    <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Mobile</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">City</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            {% for customer in customers %}
            <tr>
                <td class="px-6 py-4 whitespace-nowrap">{{ customer.customer_id }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ customer.full_name }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ customer.mobile }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ customer.city }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <a href="{% url 'customers:update' customer.pk %}" class="text-indigo-600 hover:text-indigo-900 mr-3">Edit</a>
                    <a href="{% url 'customers:detail' customer.pk %}" class="text-blue-600 hover:text-blue-900">View 360</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">No customers found.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
"""

customers_form_html = """{% extends 'dashboard/base.html' %}
{% load crispy_forms_tags %}
{% block content %}
<div class="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow">
    <h1 class="text-2xl font-bold mb-6">{% if object %}Edit Customer{% else %}Add Customer{% endif %}</h1>
    <form method="post">
        {% csrf_token %}
        <div class="grid grid-cols-2 gap-4">
            {{ form|crispy }}
        </div>
        <div class="mt-6 flex justify-end gap-4">
            <a href="{% url 'customers:list' %}" class="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300">Cancel</a>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Save</button>
        </div>
    </form>
</div>
{% endblock %}
"""

customers_detail_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="mb-6 flex justify-between items-center">
    <h1 class="text-2xl font-bold text-gray-800">Customer 360: {{ customer.full_name }}</h1>
    <a href="{% url 'customers:update' customer.pk %}" class="bg-indigo-600 text-white px-4 py-2 rounded shadow hover:bg-indigo-700">Edit Customer</a>
</div>

<div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
    <div class="bg-white rounded-lg shadow p-6 border-t-4 border-blue-500">
        <h3 class="text-sm font-medium text-gray-500">Total Purchases</h3>
        <p class="text-2xl font-bold text-gray-900">{{ orders.count }}</p>
    </div>
    <div class="bg-white rounded-lg shadow p-6 border-t-4 border-green-500">
        <h3 class="text-sm font-medium text-gray-500">Amount Spent</h3>
        <p class="text-2xl font-bold text-gray-900">₹{{ total_spent }}</p>
    </div>
    <div class="bg-white rounded-lg shadow p-6 border-t-4 border-yellow-500">
        <h3 class="text-sm font-medium text-gray-500">Warranties</h3>
        <p class="text-2xl font-bold text-gray-900">{{ warranties.count }}</p>
    </div>
    <div class="bg-white rounded-lg shadow p-6 border-t-4 border-red-500">
        <h3 class="text-sm font-medium text-gray-500">Complaints</h3>
        <p class="text-2xl font-bold text-gray-900">{{ complaints.count }}</p>
    </div>
</div>

<div class="bg-white shadow rounded-lg mb-6">
    <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8 px-6" aria-label="Tabs" id="tabs">
            <a href="#" class="border-blue-500 text-blue-600 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm" data-target="overview">Overview</a>
            <a href="#" class="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm" data-target="orders">Orders</a>
            <a href="#" class="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm" data-target="warranties">Warranties</a>
            <a href="#" class="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm" data-target="complaints">Complaints</a>
        </nav>
    </div>
    
    <div class="p-6">
        <div id="overview" class="tab-content">
            <div class="grid grid-cols-2 gap-4">
                <div><strong>Email:</strong> {{ customer.email }}</div>
                <div><strong>Mobile:</strong> {{ customer.mobile }}</div>
                <div><strong>Customer ID:</strong> {{ customer.customer_id }}</div>
                <div><strong>Type:</strong> {{ customer.get_customer_type_display }}</div>
                <div><strong>City:</strong> {{ customer.city }}</div>
                <div><strong>Status:</strong> {{ customer.get_account_status_display }}</div>
                <div class="col-span-2"><strong>Address:</strong> {{ customer.address }}</div>
            </div>
        </div>
        
        <div id="orders" class="tab-content hidden">
            <table class="min-w-full divide-y divide-gray-200">
                <thead>
                    <tr>
                        <th class="text-left py-2">Order #</th>
                        <th class="text-left py-2">Date</th>
                        <th class="text-left py-2">Status</th>
                        <th class="text-left py-2">Total</th>
                    </tr>
                </thead>
                <tbody>
                    {% for order in orders %}
                    <tr>
                        <td class="py-2">{{ order.order_number }}</td>
                        <td class="py-2">{{ order.order_date|date:"M d, Y" }}</td>
                        <td class="py-2">{{ order.get_order_status_display }}</td>
                        <td class="py-2">₹{{ order.grand_total }}</td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="4" class="py-2 text-gray-500">No orders found.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div id="warranties" class="tab-content hidden">
            <table class="min-w-full divide-y divide-gray-200">
                <thead>
                    <tr>
                        <th class="text-left py-2">Product</th>
                        <th class="text-left py-2">Serial</th>
                        <th class="text-left py-2">End Date</th>
                        <th class="text-left py-2">Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for warranty in warranties %}
                    <tr>
                        <td class="py-2">{{ warranty.product.name }}</td>
                        <td class="py-2">{{ warranty.serial_number.serial_number }}</td>
                        <td class="py-2">{{ warranty.warranty_end|date:"M d, Y" }}</td>
                        <td class="py-2">{{ warranty.get_status_display }}</td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="4" class="py-2 text-gray-500">No warranties found.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div id="complaints" class="tab-content hidden">
            <table class="min-w-full divide-y divide-gray-200">
                <thead>
                    <tr>
                        <th class="text-left py-2">Ticket ID</th>
                        <th class="text-left py-2">Subject</th>
                        <th class="text-left py-2">Status</th>
                        <th class="text-left py-2">Date</th>
                    </tr>
                </thead>
                <tbody>
                    {% for complaint in complaints %}
                    <tr>
                        <td class="py-2">{{ complaint.ticket_id }}</td>
                        <td class="py-2">{{ complaint.subject }}</td>
                        <td class="py-2">{{ complaint.get_status_display }}</td>
                        <td class="py-2">{{ complaint.created_at|date:"M d, Y" }}</td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="4" class="py-2 text-gray-500">No complaints found.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('#tabs a');
    const contents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            // Reset tabs
            tabs.forEach(t => {
                t.classList.remove('border-blue-500', 'text-blue-600');
                t.classList.add('border-transparent', 'text-gray-500');
            });
            // Set active tab
            this.classList.remove('border-transparent', 'text-gray-500');
            this.classList.add('border-blue-500', 'text-blue-600');
            
            // Hide all content
            contents.forEach(c => c.classList.add('hidden'));
            // Show target content
            document.getElementById(this.dataset.target).classList.remove('hidden');
        });
    });
});
</script>
{% endblock %}
"""

write_file(f"{base_dir}/customers/views.py", customers_views)
write_file(f"{base_dir}/customers/urls.py", customers_urls)
write_file(f"{base_dir}/customers/forms.py", customers_forms)
write_file(f"{base_dir}/templates/customers/customer_list.html", customers_list_html)
write_file(f"{base_dir}/templates/customers/customer_form.html", customers_form_html)
write_file(f"{base_dir}/templates/customers/customer_detail.html", customers_detail_html)

print("Customers module generated.")

