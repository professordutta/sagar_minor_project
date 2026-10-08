import uuid
from django.db import models
from django.conf import settings
from core.models import TimeStampedModel


class Order(TimeStampedModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('ready_for_delivery', 'Ready for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    order_number = models.CharField(max_length=30, unique=True, db_index=True)
    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.PROTECT, related_name='orders'
    )
    order_date = models.DateTimeField(auto_now_add=True)
    salesperson = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='sales_orders'
    )
    store_branch = models.CharField(max_length=100, blank=True)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    shipping = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending'
    )
    order_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['customer']),
            models.Index(fields=['-order_date']),
        ]

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def _generate_order_number(self):
        import random
        from django.utils import timezone
        year = timezone.now().year
        while True:
            num = f'ORD-{year}-{random.randint(10000, 99999)}'
            if not Order.objects.filter(order_number=num).exists():
                return num

    @property
    def item_count(self):
        return self.items.count()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    serial_number = models.ForeignKey(
        'products.SerialNumber', on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = 'Order Item'

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'


class Invoice(TimeStampedModel):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('refunded', 'Refunded'),
    ]

    invoice_number = models.CharField(max_length=30, unique=True, db_index=True)
    invoice_date = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.PROTECT, related_name='invoices'
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    billing_address = models.TextField(blank=True)
    shipping_address = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2)
    tax = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=14, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    gst_number = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-invoice_date']
        indexes = [models.Index(fields=['invoice_number'])]

    def __str__(self):
        return self.invoice_number

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self._generate_invoice_number()
        super().save(*args, **kwargs)

    def _generate_invoice_number(self):
        import random
        from django.utils import timezone
        year = timezone.now().year
        while True:
            num = f'INV-{year}-{random.randint(10000, 99999)}'
            if not Invoice.objects.filter(invoice_number=num).exists():
                return num


class ReturnRequest(TimeStampedModel):
    RETURN_TYPE_CHOICES = [
        ('return', 'Return'),
        ('replacement', 'Replacement'),
        ('refund', 'Refund'),
        ('exchange', 'Exchange'),
    ]
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pickup_scheduled', 'Pickup Scheduled'),
        ('received', 'Received'),
        ('inspected', 'Inspected'),
        ('refunded', 'Refunded'),
        ('replaced', 'Replaced'),
        ('closed', 'Closed'),
    ]

    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='returns')
    order_item = models.ForeignKey(OrderItem, on_delete=models.PROTECT)
    return_type = models.CharField(max_length=20, choices=RETURN_TYPE_CHOICES)
    reason = models.TextField()
    condition = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    approval_notes = models.TextField(blank=True)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    handled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Return for {self.order.order_number} - {self.return_type}'

