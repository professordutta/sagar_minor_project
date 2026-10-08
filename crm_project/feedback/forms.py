from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['complaint', 'service_request', 'rating', 'comments', 'is_public']
