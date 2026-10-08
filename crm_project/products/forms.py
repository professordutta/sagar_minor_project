from django import forms
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
