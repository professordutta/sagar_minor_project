from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['customer', 'order', 'product', 'serial_number', 'category', 'subject', 'description', 'priority', 'status', 'assigned_to']
