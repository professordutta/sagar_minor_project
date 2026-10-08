from django.db import models
from core.models import TimeStampedModel
from brands.models import Brand
from categories.models import Category

class Product(TimeStampedModel):
    STATUS_CHOICES = [('active','Active'),('inactive','Inactive'),('discontinued','Discontinued')]
    WARRANTY_TYPE_CHOICES = [('manufacturer','Manufacturer'),('extended','Extended'),('amc','AMC'),('none','None')]

    sku = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    model_number = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    mrp = models.DecimalField(max_digits=12, decimal_places=2)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    warranty_period = models.PositiveIntegerField(default=12, help_text='Warranty in months')
    warranty_type = models.CharField(max_length=20, choices=WARRANTY_TYPE_CHOICES, default='manufacturer')
    requires_serial_tracking = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.sku})'

class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=200, blank=True)

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=500)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'key']
        unique_together = ['product', 'key']

class SerialNumber(TimeStampedModel):
    STATUS_CHOICES = [
        ('in_stock','In Stock'),
        ('sold','Sold'),
        ('returned','Returned'),
        ('under_service','Under Service'),
        ('warranty_claim','Warranty Claim'),
        ('scrapped','Scrapped'),
    ]
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='serial_numbers')
    serial_number = models.CharField(max_length=100, unique=True, db_index=True)
    customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    warranty_start = models.DateField(null=True, blank=True)
    warranty_end = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock')

    def __str__(self):
        return f'{self.serial_number} - {self.product.name}'
