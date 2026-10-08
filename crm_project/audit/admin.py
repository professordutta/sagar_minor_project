from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'object_repr', 'ip_address', 'created_at']
    list_filter = ['action']
    readonly_fields = [
        'user', 'action', 'content_type', 'object_id', 'object_repr',
        'old_value', 'new_value', 'ip_address', 'user_agent', 'created_at'
    ]
    search_fields = ['user__email', 'object_repr']
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

