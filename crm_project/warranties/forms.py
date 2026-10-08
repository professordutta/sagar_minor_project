from django import forms
from .models import Warranty


class WarrantyForm(forms.ModelForm):
    class Meta:
        model = Warranty
        fields = [
            'customer', 'product', 'serial_number', 'invoice',
            'purchase_date', 'warranty_start', 'warranty_end',
            'warranty_type', 'is_extended', 'terms',
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_start': forms.DateInput(attrs={'type': 'date'}),
            'warranty_end': forms.DateInput(attrs={'type': 'date'}),
            'terms': forms.Textarea(attrs={'rows': 3}),
        }
