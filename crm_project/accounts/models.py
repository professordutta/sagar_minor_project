import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)
    employee_id = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'

    @property
    def full_name(self):
        return self.get_full_name() or self.email

    @property
    def primary_role(self):
        if self.is_superuser:
            return 'super_admin'
        group = self.groups.first()
        return group.name if group else None

    def has_role(self, *roles):
        if self.is_superuser:
            return True
        return self.groups.filter(name__in=roles).exists()

    def is_staff_member(self):
        return self.is_staff or self.has_role('super_admin', 'crm_staff', 'service_agent', 'sales_staff', 'technician')

    def is_customer_user(self):
        return self.has_role('customer') and not self.is_staff

    def get_dashboard_url(self):
        role = self.primary_role
        if role in ('super_admin', 'crm_staff'):
            return '/dashboard/admin/'
        elif role == 'service_agent':
            return '/dashboard/service-agent/'
        elif role == 'sales_staff':
            return '/dashboard/sales/'
        elif role == 'technician':
            return '/dashboard/technician/'
        elif role == 'customer':
            return '/dashboard/customer/'
        return '/dashboard/'
