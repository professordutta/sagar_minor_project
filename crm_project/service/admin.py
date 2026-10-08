from django.contrib import admin
from .models import ServiceRequest, ServicePart, ServiceNote


class ServicePartInline(admin.TabularInline):
    model = ServicePart
    extra = 0


class ServiceNoteInline(admin.TabularInline):
    model = ServiceNote
    extra = 0
    readonly_fields = ['created_at']


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = [
        'service_id', 'customer', 'product', 'service_type',
        'status', 'technician', 'scheduled_date'
    ]
    list_filter = ['status', 'service_type']
    search_fields = [
        'service_id', 'customer__first_name', 'customer__mobile',
        'product__name'
    ]
    readonly_fields = ['service_id', 'created_at', 'updated_at']
    inlines = [ServicePartInline, ServiceNoteInline]
    date_hierarchy = 'created_at'

