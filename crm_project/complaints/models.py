from django.db import models
from django.conf import settings
from core.models import TimeStampedModel


class Complaint(TimeStampedModel):
    CATEGORY_CHOICES = [
        ('product_issue', 'Product Issue'),
        ('installation', 'Installation'),
        ('delivery', 'Delivery'),
        ('warranty', 'Warranty'),
        ('payment', 'Payment'),
        ('billing', 'Billing'),
        ('service', 'Service'),
        ('replacement', 'Replacement'),
        ('refund', 'Refund'),
        ('other', 'Other'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('waiting_for_customer', 'Waiting for Customer'),
        ('waiting_for_vendor', 'Waiting for Vendor'),
        ('escalated', 'Escalated'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
    ]

    ticket_id = models.CharField(max_length=25, unique=True, db_index=True)
    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.PROTECT, related_name='complaints'
    )
    order = models.ForeignKey(
        'orders.Order', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='complaints'
    )
    product = models.ForeignKey(
        'products.Product', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='complaints'
    )
    serial_number = models.ForeignKey(
        'products.SerialNumber', on_delete=models.SET_NULL, null=True, blank=True
    )
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_complaints'
    )
    expected_resolution_date = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    sla_breach = models.BooleanField(default=False)
    escalation_level = models.PositiveSmallIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ticket_id']),
            models.Index(fields=['customer']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'{self.ticket_id}: {self.subject}'

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            from core.utils import generate_unique_id
            self.ticket_id = generate_unique_id('TKT', Complaint, 'ticket_id')
        super().save(*args, **kwargs)

    def set_sla_deadline(self):
        """Set expected resolution date based on priority SLA config."""
        from django.conf import settings
        from django.utils import timezone
        from datetime import timedelta

        sla_config = getattr(settings, 'SLA_DEFAULTS', {})
        hours = sla_config.get(self.priority, {}).get('resolution', 24)
        self.expected_resolution_date = timezone.now() + timedelta(hours=hours)

    @property
    def sla_remaining_hours(self):
        if not self.expected_resolution_date:
            return None
        from django.utils import timezone
        delta = self.expected_resolution_date - timezone.now()
        return delta.total_seconds() / 3600

    @property
    def sla_status(self):
        remaining = self.sla_remaining_hours
        if remaining is None:
            return 'no_sla'
        if self.status in ('resolved', 'closed'):
            return 'resolved'
        if remaining < 0:
            return 'breached'
        if remaining < 2:
            return 'at_risk'
        return 'ok'


class ComplaintActivity(models.Model):
    """Immutable timeline entry for a complaint."""
    complaint = models.ForeignKey(
        Complaint, on_delete=models.CASCADE, related_name='activities'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    action = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    is_internal = models.BooleanField(
        default=False,
        help_text='Internal notes are visible only to staff'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Complaint Activity'
        verbose_name_plural = 'Complaint Activities'

    def __str__(self):
        return f'{self.complaint.ticket_id} - {self.action}'


class ComplaintAssignment(models.Model):
    """History of complaint assignment changes."""
    complaint = models.ForeignKey(
        Complaint, on_delete=models.CASCADE, related_name='assignments'
    )
    previous_assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='previous_assignments'
    )
    new_assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='new_assignments'
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assignment_changes'
    )
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class SLAConfig(models.Model):
    """Configurable SLA rules per priority."""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, unique=True)
    response_hours = models.PositiveIntegerField(default=8)
    resolution_hours = models.PositiveIntegerField(default=24)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'SLA Configuration'

    def __str__(self):
        return f'SLA: {self.priority} — {self.resolution_hours}h resolution'

