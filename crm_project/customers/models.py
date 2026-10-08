import uuid
from django.db import models
from django.conf import settings
from django.urls import reverse
from core.models import TimeStampedModel

class Customer(TimeStampedModel):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('N', 'Prefer not to say')]
    CUSTOMER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('vip', 'VIP'),
        ('corporate', 'Corporate'),
        ('institutional', 'Institutional'),
    ]
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive'), ('blocked', 'Blocked')]
    CONTACT_CHOICES = [('phone', 'Phone'), ('email', 'Email'), ('sms', 'SMS'), ('whatsapp', 'WhatsApp')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='customer_profile'
    )
    customer_id = models.CharField(max_length=20, unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, db_index=True)
    alternate_mobile = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pin_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=100, default='India')
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='individual')
    preferred_contact = models.CharField(max_length=20, choices=CONTACT_CHOICES, default='phone')
    account_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['mobile']),
            models.Index(fields=['email']),
            models.Index(fields=['customer_id']),
        ]

    def __str__(self):
        return f'{self.full_name} ({self.customer_id})'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def get_absolute_url(self):
        return reverse('customers:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.customer_id:
            self.customer_id = self._generate_customer_id()
        super().save(*args, **kwargs)

    def _generate_customer_id(self):
        import random
        from django.utils import timezone
        year = timezone.now().year
        while True:
            cid = f'CUS-{year}-{random.randint(10000, 99999)}'
            if not Customer.objects.filter(customer_id=cid).exists():
                return cid
