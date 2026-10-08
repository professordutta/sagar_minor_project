from django.db import models
from core.models import TimeStampedModel


class Warranty(TimeStampedModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expiring_soon', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('claimed', 'Claimed'),
        ('void', 'Void'),
    ]
    WARRANTY_TYPE_CHOICES = [
        ('manufacturer', 'Manufacturer'),
        ('extended', 'Extended'),
        ('amc', 'AMC'),
    ]

    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.PROTECT, related_name='warranties'
    )
    product = models.ForeignKey(
        'products.Product', on_delete=models.PROTECT, related_name='warranties'
    )
    serial_number = models.ForeignKey(
        'products.SerialNumber', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='warranties'
    )
    invoice = models.ForeignKey(
        'orders.Invoice', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='warranties'
    )
    purchase_date = models.DateField()
    warranty_start = models.DateField()
    warranty_end = models.DateField()
    warranty_type = models.CharField(
        max_length=20, choices=WARRANTY_TYPE_CHOICES, default='manufacturer'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_extended = models.BooleanField(default=False)
    terms = models.TextField(blank=True)
    registered_by_customer = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Warranties'
        ordering = ['-warranty_end']
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['status']),
            models.Index(fields=['warranty_end']),
        ]

    def __str__(self):
        return f'Warranty: {self.product.name} — {self.customer.full_name}'

    @property
    def days_remaining(self):
        from datetime import date
        return (self.warranty_end - date.today()).days

    @property
    def computed_status(self):
        from core.utils import get_warranty_status
        return get_warranty_status(self.warranty_end)

    @property
    def status_display(self):
        from core.utils import get_warranty_display
        return get_warranty_display(self.warranty_end)

    def update_status(self):
        """Recalculate and save warranty status based on current date."""
        new_status = self.computed_status
        if self.status != new_status and self.status not in ('claimed', 'void'):
            self.status = new_status
            self.save(update_fields=['status'])

