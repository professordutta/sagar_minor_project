from django import forms
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
