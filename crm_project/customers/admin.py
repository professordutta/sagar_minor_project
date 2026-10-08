from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'full_name', 'email', 'mobile', 'customer_type', 'account_status', 'created_at']
    list_filter = ['customer_type', 'account_status', 'gender']
    search_fields = ['customer_id', 'first_name', 'last_name', 'email', 'mobile']
    readonly_fields = ['customer_id', 'created_at', 'updated_at']
