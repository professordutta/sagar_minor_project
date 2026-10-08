from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Order, Invoice
from .forms import OrderForm, InvoiceForm


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    queryset = Order.objects.filter(is_deleted=False).select_related('customer')


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:list')


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:list')


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.select_related('product')
        context['invoice'] = Invoice.objects.filter(order=self.object).first()
        return context


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'orders/invoice_list.html'
    context_object_name = 'invoices'


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'orders/invoice_detail.html'
    context_object_name = 'invoice'
