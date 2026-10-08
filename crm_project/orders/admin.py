from django.contrib import admin
from .models import Order, OrderItem, Invoice, ReturnRequest


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'customer', 'grand_total', 'order_status',
        'payment_status', 'order_date'
    ]
    list_filter = ['order_status', 'payment_status']
    search_fields = ['order_number', 'customer__first_name', 'customer__mobile']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    date_hierarchy = 'order_date'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer', 'grand_total', 'payment_status', 'invoice_date']
    search_fields = ['invoice_number', 'customer__first_name', 'customer__mobile']
    readonly_fields = ['invoice_number', 'created_at', 'updated_at']


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ['order', 'return_type', 'status', 'created_at']
    list_filter = ['return_type', 'status']

