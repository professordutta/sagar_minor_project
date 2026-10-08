from django.contrib import admin
from .models import Complaint, ComplaintActivity, ComplaintAssignment, SLAConfig


class ActivityInline(admin.TabularInline):
    model = ComplaintActivity
    extra = 0
    readonly_fields = ['created_at', 'actor', 'action', 'notes', 'is_internal']
    can_delete = False


class AssignmentInline(admin.TabularInline):
    model = ComplaintAssignment
    extra = 0
    readonly_fields = ['previous_assignee', 'new_assignee', 'changed_by', 'reason', 'created_at']
    can_delete = False


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = [
        'ticket_id', 'customer', 'subject', 'priority', 'status',
        'assigned_to', 'sla_breach', 'created_at'
    ]
    list_filter = ['priority', 'status', 'category', 'sla_breach']
    search_fields = ['ticket_id', 'subject', 'customer__first_name', 'customer__mobile']
    readonly_fields = ['ticket_id', 'created_at', 'updated_at']
    inlines = [ActivityInline, AssignmentInline]
    date_hierarchy = 'created_at'


@admin.register(SLAConfig)
class SLAConfigAdmin(admin.ModelAdmin):
    list_display = ['priority', 'response_hours', 'resolution_hours', 'is_active']

