from django.db import models
from django.conf import settings
from core.models import TimeStampedModel


class ServiceRequest(TimeStampedModel):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('scheduled', 'Scheduled'),
        ('technician_assigned', 'Technician Assigned'),
        ('technician_on_way', 'Technician On The Way'),
        ('visit_completed', 'Visit Completed'),
        ('parts_required', 'Parts Required'),
        ('repair_in_progress', 'Repair In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    SERVICE_TYPE_CHOICES = [
        ('installation', 'Installation'),
        ('repair', 'Repair'),
        ('maintenance', 'Maintenance'),
        ('inspection', 'Inspection'),
        ('replacement', 'Replacement'),
    ]

    service_id = models.CharField(max_length=25, unique=True, db_index=True)
    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.PROTECT, related_name='service_requests'
    )
    product = models.ForeignKey(
        'products.Product', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='service_requests'
    )
    serial_number = models.ForeignKey(
        'products.SerialNumber', on_delete=models.SET_NULL, null=True, blank=True
    )
    warranty = models.ForeignKey(
        'warranties.Warranty', on_delete=models.SET_NULL, null=True, blank=True
    )
    complaint = models.ForeignKey(
        'complaints.Complaint', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='service_requests'
    )
    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='service_requests'
    )
    scheduled_date = models.DateTimeField(null=True, blank=True)
    visit_date = models.DateTimeField(null=True, blank=True)
    service_type = models.CharField(
        max_length=20, choices=SERVICE_TYPE_CHOICES, default='repair'
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='requested')
    notes = models.TextField(blank=True)
    service_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customer_acknowledgement = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['service_id']),
            models.Index(fields=['customer']),
            models.Index(fields=['technician']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.service_id

    def save(self, *args, **kwargs):
        if not self.service_id:
            from core.utils import generate_unique_id
            self.service_id = generate_unique_id('SRV', ServiceRequest, 'service_id')
        super().save(*args, **kwargs)


class ServicePart(models.Model):
    """Parts used in a service request."""
    service_request = models.ForeignKey(
        ServiceRequest, on_delete=models.CASCADE, related_name='parts'
    )
    part_name = models.CharField(max_length=200)
    part_number = models.CharField(max_length=100, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def total_cost(self):
        return self.quantity * self.unit_cost

    def __str__(self):
        return f'{self.part_name} x{self.quantity}'


class ServiceNote(models.Model):
    """Notes added during a service request."""
    service_request = models.ForeignKey(
        ServiceRequest, on_delete=models.CASCADE, related_name='service_notes'
    )
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    note = models.TextField()
    is_internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

