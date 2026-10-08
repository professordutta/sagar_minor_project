from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['customer', 'rating', 'complaint', 'service_request', 'created_at']
    list_filter = ['rating']
    search_fields = ['customer__first_name', 'customer__mobile', 'comments']
    date_hierarchy = 'created_at'

