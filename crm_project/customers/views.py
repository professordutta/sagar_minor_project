from django.urls import reverse_lazy
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
