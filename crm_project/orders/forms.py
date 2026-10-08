from django import forms
from .models import Order, OrderItem, Invoice


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer', 'store_branch', 'salesperson',
            'subtotal', 'discount', 'tax', 'shipping', 'grand_total',
            'payment_status', 'order_status', 'notes',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = [
            'product', 'quantity', 'unit_price', 'discount', 'tax',
            'total', 'serial_number',
        ]


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'customer', 'order',
            'billing_address', 'shipping_address',
            'subtotal', 'tax', 'grand_total',
            'payment_status', 'notes',
        ]
        widgets = {
            'billing_address': forms.Textarea(attrs={'rows': 3}),
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
