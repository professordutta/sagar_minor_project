from django.contrib import admin
from .models import Warranty


@admin.register(Warranty)
class WarrantyAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'customer', 'serial_number', 'warranty_start',
        'warranty_end', 'status', 'warranty_type'
    ]
    list_filter = ['status', 'warranty_type', 'is_extended']
    search_fields = [
        'customer__first_name', 'customer__mobile',
        'product__name', 'serial_number__serial_number'
    ]
    date_hierarchy = 'warranty_end'
    readonly_fields = ['created_at', 'updated_at']

