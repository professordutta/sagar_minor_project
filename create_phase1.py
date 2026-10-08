import os

BASE_DIR = r"D:\sagar_minor_project"

files = {
    "requirements.txt": """Django==4.2.16
djangorestframework==3.15.2
django-environ==0.11.2
Pillow==10.4.0
django-crispy-forms==2.3
crispy-tailwind==1.0.3
django-extensions==3.2.3
whitenoise==6.7.0
gunicorn==23.0.0
psycopg2-binary==2.9.9
django-filter==24.3
openpyxl==3.1.5
reportlab==4.2.5
""",
    ".env.example": """SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=CRM System <noreply@example.com>
MEDIA_ROOT=media
STATIC_ROOT=staticfiles
""",
    ".gitignore": """venv/
.env
__pycache__/
*.pyc
*.pyo
db.sqlite3
media/
staticfiles/
.DS_Store
*.log
.idea/
.vscode/
*.egg-info/
dist/
build/
""",
    r"crm_project\manage.py": """#!/usr/bin/env python
\"\"\"Django's command-line utility for administrative tasks.\"\"\"
import os
import sys

def main():
    \"\"\"Run administrative tasks.\"\"\"
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
""",
    r"crm_project\crm_project\__init__.py": "",
    r"crm_project\crm_project\settings.py": """import os
from pathlib import Path
import environ

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment
env = environ.Env(
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list, ['localhost', '127.0.0.1']),
)

# Read .env file from project root (parent of crm_project/)
env_file = BASE_DIR.parent / '.env'
if env_file.exists():
    environ.Env.read_env(env_file)

SECRET_KEY = env('SECRET_KEY', default='django-insecure-dev-key-change-this-in-production-xyz123')
DEBUG = env('DEBUG', default=True)
ALLOWED_HOSTS = env('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Third party
    'rest_framework',
    'crispy_forms',
    'crispy_tailwind',
    'django_filters',
    'django_extensions',
    # Local apps
    'core.apps.CoreConfig',
    'accounts.apps.AccountsConfig',
    'customers.apps.CustomersConfig',
    'brands.apps.BrandsConfig',
    'categories.apps.CategoriesConfig',
    'products.apps.ProductsConfig',
    'orders.apps.OrdersConfig',
    'warranties.apps.WarrantiesConfig',
    'complaints.apps.ComplaintsConfig',
    'service.apps.ServiceConfig',
    'notifications.apps.NotificationsConfig',
    'feedback.apps.FeedbackConfig',
    'reports.apps.ReportsConfig',
    'dashboard.apps.DashboardConfig',
    'audit.apps.AuditConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'audit.middleware.AuditMiddleware',
]

ROOT_URLCONF = 'crm_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.global_context',
                'notifications.context_processors.notifications_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'crm_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='CRM System <noreply@example.com>')

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

CRM_PAGE_SIZE = 25

SLA_DEFAULTS = {
    'critical': {'response': 1, 'resolution': 4},
    'high': {'response': 2, 'resolution': 8},
    'medium': {'response': 4, 'resolution': 24},
    'low': {'response': 8, 'resolution': 48},
}
""",
    r"crm_project\crm_project\urls.py": """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('customers/', include('customers.urls', namespace='customers')),
    path('brands/', include('brands.urls', namespace='brands')),
    path('categories/', include('categories.urls', namespace='categories')),
    path('products/', include('products.urls', namespace='products')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('warranties/', include('warranties.urls', namespace='warranties')),
    path('complaints/', include('complaints.urls', namespace='complaints')),
    path('service/', include('service.urls', namespace='service')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('feedback/', include('feedback.urls', namespace='feedback')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('audit/', include('audit.urls', namespace='audit')),
    path('api/v1/', include('core.api_urls', namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'core.views.error_400'
handler403 = 'core.views.error_403'
handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'
""",
    r"crm_project\crm_project\wsgi.py": """import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
application = get_wsgi_application()
""",
    r"crm_project\crm_project\asgi.py": """import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
application = get_asgi_application()
""",
    r"crm_project\core\__init__.py": "",
    r"crm_project\core\apps.py": """from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Core'
""",
    r"crm_project\core\models.py": """import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class TimeStampedModel(models.Model):
    \"\"\"Abstract base model with created/updated timestamps.\"\"\"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    \"\"\"Abstract base model with soft delete support.\"\"\"
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='%(app_label)s_%(class)s_deleted'
    )

    class Meta:
        abstract = True

    def soft_delete(self, user=None):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save(update_fields=['is_deleted', 'deleted_at', 'deleted_by'])

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=['is_deleted', 'deleted_at', 'deleted_by'])


class BaseModel(TimeStampedModel, SoftDeleteModel):
    \"\"\"Combined base model with timestamps and soft delete.\"\"\"
    class Meta:
        abstract = True


class ActiveManager(models.Manager):
    \"\"\"Manager that excludes soft-deleted records.\"\"\"
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
""",
    r"crm_project\core\mixins.py": """from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    \"\"\"Mixin to require specific user roles.\"\"\"
    allowed_roles = []  # List of role names (group names)

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if not self.allowed_roles:
            return True
        return user.groups.filter(name__in=self.allowed_roles).exists()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied


class CustomerAccessMixin(LoginRequiredMixin):
    \"\"\"Mixin for customer-only views. Ensures customers access only their own data.\"\"\"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not hasattr(request.user, 'customer_profile'):
            messages.error(request, 'Customer profile not found.')
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)


class StaffRequiredMixin(RoleRequiredMixin):
    \"\"\"Requires the user to be staff (any non-customer role).\"\"\"
    allowed_roles = ['super_admin', 'crm_staff', 'service_agent', 'sales_staff', 'technician']


class AdminRequiredMixin(RoleRequiredMixin):
    \"\"\"Requires super_admin or crm_staff.\"\"\"
    allowed_roles = ['super_admin', 'crm_staff']


class SuperAdminMixin(RoleRequiredMixin):
    \"\"\"Requires super_admin.\"\"\"
    allowed_roles = ['super_admin']
""",
    r"crm_project\core\context_processors.py": """from django.conf import settings

def global_context(request):
    \"\"\"Add global context variables to all templates.\"\"\"
    context = {
        'APP_NAME': 'VijayaCRM',
        'APP_VERSION': '1.0.0',
        'DEBUG': settings.DEBUG,
    }
    if request.user.is_authenticated:
        context['user_role'] = get_user_role(request.user)
        context['is_super_admin'] = request.user.is_superuser or request.user.groups.filter(name='super_admin').exists()
        context['is_crm_staff'] = request.user.groups.filter(name='crm_staff').exists()
        context['is_service_agent'] = request.user.groups.filter(name='service_agent').exists()
        context['is_sales_staff'] = request.user.groups.filter(name='sales_staff').exists()
        context['is_technician'] = request.user.groups.filter(name='technician').exists()
        context['is_customer'] = request.user.groups.filter(name='customer').exists()
        context['is_staff_user'] = (
            request.user.is_staff or
            request.user.groups.filter(name__in=['super_admin', 'crm_staff', 'service_agent', 'sales_staff', 'technician']).exists()
        )
    return context

def get_user_role(user):
    if user.is_superuser:
        return 'super_admin'
    group = user.groups.first()
    return group.name if group else 'unknown'
""",
    r"crm_project\core\views.py": """from django.shortcuts import render

def error_400(request, exception=None):
    return render(request, 'errors/400.html', status=400)

def error_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def error_404(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def error_500(request):
    return render(request, 'errors/500.html', status=500)
""",
    r"crm_project\core\utils.py": """import random
import string
from datetime import date
from django.utils import timezone


def generate_unique_id(prefix, model_class, field_name, length=6):
    \"\"\"Generate a unique ID like TKT-2026-000001.\"\"\"
    year = timezone.now().year
    while True:
        number = ''.join(random.choices(string.digits, k=length))
        uid = f"{prefix}-{year}-{number}"
        if not model_class.objects.filter(**{field_name: uid}).exists():
            return uid


def get_warranty_status(warranty_end_date):
    \"\"\"Calculate warranty status from end date.\"\"\"
    today = date.today()
    if warranty_end_date < today:
        return 'expired'
    days_remaining = (warranty_end_date - today).days
    if days_remaining <= 30:
        return 'expiring_soon'
    return 'active'


def get_warranty_display(warranty_end_date):
    \"\"\"Get human-readable warranty status.\"\"\"
    today = date.today()
    delta = (warranty_end_date - today).days
    if delta < 0:
        return f'Expired {abs(delta)} days ago'
    elif delta == 0:
        return 'Expires today'
    elif delta <= 30:
        return f'Expires in {delta} days'
    else:
        months = delta // 30
        return f'Expires in ~{months} months'
""",
    r"crm_project\core\api_urls.py": """from django.urls import path

app_name = 'api'

urlpatterns = [
    # API endpoints will be added per module
]
""",
    r"crm_project\core\templatetags\__init__.py": "",
    r"crm_project\core\templatetags\crm_tags.py": """from django import template
from django.utils.safestring import mark_safe
from datetime import date

register = template.Library()

@register.filter
def status_badge(value, badge_type=None):
    \"\"\"Render a colored status badge.\"\"\"
    badge_map = {
        'pending': ('yellow', 'Pending'),
        'confirmed': ('blue', 'Confirmed'),
        'processing': ('indigo', 'Processing'),
        'ready_for_delivery': ('purple', 'Ready'),
        'delivered': ('green', 'Delivered'),
        'cancelled': ('red', 'Cancelled'),
        'returned': ('gray', 'Returned'),
        'paid': ('green', 'Paid'),
        'partially_paid': ('yellow', 'Partial'),
        'refunded': ('red', 'Refunded'),
        'active': ('green', 'Active'),
        'expiring_soon': ('yellow', 'Expiring Soon'),
        'expired': ('red', 'Expired'),
        'claimed': ('blue', 'Claimed'),
        'void': ('gray', 'Void'),
        'open': ('blue', 'Open'),
        'assigned': ('indigo', 'Assigned'),
        'in_progress': ('purple', 'In Progress'),
        'waiting_for_customer': ('yellow', 'Waiting - Customer'),
        'waiting_for_vendor': ('orange', 'Waiting - Vendor'),
        'escalated': ('red', 'Escalated'),
        'resolved': ('green', 'Resolved'),
        'closed': ('gray', 'Closed'),
        'rejected': ('red', 'Rejected'),
        'low': ('gray', 'Low'),
        'medium': ('blue', 'Medium'),
        'high': ('orange', 'High'),
        'critical': ('red', 'Critical'),
    }
    color, label = badge_map.get(str(value).lower(), ('gray', str(value).title()))
    color_classes = {
        'green': 'bg-green-100 text-green-800',
        'yellow': 'bg-yellow-100 text-yellow-800',
        'red': 'bg-red-100 text-red-800',
        'blue': 'bg-blue-100 text-blue-800',
        'indigo': 'bg-indigo-100 text-indigo-800',
        'purple': 'bg-purple-100 text-purple-800',
        'orange': 'bg-orange-100 text-orange-800',
        'gray': 'bg-gray-100 text-gray-700',
    }
    css = color_classes.get(color, 'bg-gray-100 text-gray-700')
    return mark_safe(
        f'<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {css}">'
        f'{label}</span>'
    )

@register.filter
def days_until(value):
    if not value:
        return ''
    today = date.today()
    if hasattr(value, 'date'):
        value = value.date()
    delta = (value - today).days
    if delta < 0:
        return f'{abs(delta)} days ago'
    elif delta == 0:
        return 'Today'
    return f'In {delta} days'

@register.simple_tag(takes_context=True)
def active_nav(context, *urls):
    \"\"\"Return 'active' class if current URL matches.\"\"\"
    request = context.get('request')
    if request:
        for url in urls:
            if request.path.startswith(url):
                return 'active'
    return ''

@register.filter
def currency(value):
    \"\"\"Format as Indian currency.\"\"\"
    try:
        return f'₹{float(value):,.2f}'
    except (TypeError, ValueError):
        return value

@register.filter
def percentage(value, total):
    try:
        return f'{(float(value) / float(total) * 100):.1f}%'
    except (TypeError, ValueError, ZeroDivisionError):
        return '0%'
""",
    r"crm_project\core\admin.py": """from django.contrib import admin
# Core app admin is minimal — models are abstract
""",
    r"crm_project\accounts\__init__.py": "",
    r"crm_project\accounts\apps.py": """from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Accounts'

    def ready(self):
        import accounts.signals  # noqa
""",
    r"crm_project\accounts\models.py": """import uuid
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
""",
    r"crm_project\accounts\forms.py": """from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_('Email Address'),
        widget=forms.EmailInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'you@example.com',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': '••••••••',
        })
    )
    remember_me = forms.BooleanField(required=False, label=_('Remember me'))

class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'you@example.com',
        })
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'First name',
        })
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Last name',
        })
    )
    mobile = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': '+91 98765 43210',
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': '••••••••',
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': '••••••••',
        })
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'mobile', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.mobile = self.cleaned_data.get('mobile')
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile', 'avatar', 'department']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'mobile': forms.TextInput(attrs={'class': 'form-input'}),
            'department': forms.TextInput(attrs={'class': 'form-input'}),
        }

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text='Temporary password for the user.'
    )
    role = forms.ChoiceField(choices=[
        ('crm_staff', 'CRM Staff'),
        ('service_agent', 'Service Agent'),
        ('sales_staff', 'Sales Staff'),
        ('technician', 'Technician'),
    ])

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'mobile', 'department', 'employee_id']
""",
    r"crm_project\accounts\views.py": """from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.groups import Group
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LoginForm, CustomerRegistrationForm, ProfileUpdateForm

User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            remember = form.cleaned_data.get('remember_me')
            if not remember:
                request.session.set_expiry(0)
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.email}!')
            next_url = request.GET.get('next', user.get_dashboard_url())
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password. Please try again.')

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out successfully.')
        return redirect('accounts:login')
    return render(request, 'accounts/logout_confirm.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())

    form = CustomerRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            from django.contrib.auth.models import Group
            customer_group, _ = Group.objects.get_or_create(name='customer')
            user.groups.add(customer_group)
            try:
                from customers.models import Customer
                Customer.objects.create(
                    user=user,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    mobile=user.mobile or '',
                )
            except Exception:
                pass
            login(request, user)
            messages.success(request, f'Welcome to VijayaCRM, {user.first_name}! Your account has been created.')
            return redirect('dashboard:customer_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')

    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def change_password_view(request):
    from django.contrib.auth.forms import PasswordChangeForm
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('accounts:profile')
    return render(request, 'accounts/change_password.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/emails/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
""",
    r"crm_project\accounts\urls.py": """from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
""",
    r"crm_project\accounts\admin.py": """from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'primary_role', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'groups']
    search_fields = ['email', 'first_name', 'last_name', 'mobile']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'mobile', 'avatar')}),
        (_('Work info'), {'fields': ('department', 'employee_id')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    def primary_role(self, obj):
        return obj.primary_role
    primary_role.short_description = 'Role'
""",
    r"crm_project\accounts\signals.py": """from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created and instance.groups.filter(name='customer').exists():
        try:
            from customers.models import Customer
            if not hasattr(instance, 'customer_profile'):
                Customer.objects.get_or_create(
                    user=instance,
                    defaults={
                        'first_name': instance.first_name,
                        'last_name': instance.last_name,
                        'email': instance.email,
                        'mobile': instance.mobile or '',
                    }
                )
        except Exception:
            pass
""",
    r"crm_project\accounts\management\__init__.py": "",
    r"crm_project\accounts\management\commands\__init__.py": "",
    r"crm_project\accounts\management\commands\setup_roles.py": """from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Setup default roles and permissions'

    def handle(self, *args, **kwargs):
        roles = [
            'super_admin',
            'crm_staff',
            'service_agent',
            'sales_staff',
            'technician',
            'customer',
        ]
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created role: {role}'))
            else:
                self.stdout.write(f'Role already exists: {role}')

        self.stdout.write(self.style.SUCCESS('All roles set up successfully.'))
""",
    r"crm_project\customers\__init__.py": "",
    r"crm_project\customers\apps.py": """from django.apps import AppConfig
class CustomersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customers'
    verbose_name = 'Customers'
""",
    r"crm_project\customers\models.py": """import uuid
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
""",
    r"crm_project\customers\views.py": """from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer

@login_required
def customer_list(request):
    customers = Customer.objects.filter(is_deleted=False).order_by('-created_at')
    return render(request, 'customers/list.html', {'customers': customers})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk, is_deleted=False)
    return render(request, 'customers/detail.html', {'customer': customer})
""",
    r"crm_project\customers\urls.py": """from django.urls import path
from . import views
app_name = 'customers'
urlpatterns = [
    path('', views.customer_list, name='list'),
    path('<uuid:pk>/', views.customer_detail, name='detail'),
]
""",
    r"crm_project\customers\admin.py": """from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'full_name', 'email', 'mobile', 'customer_type', 'account_status', 'created_at']
    list_filter = ['customer_type', 'account_status', 'gender']
    search_fields = ['customer_id', 'first_name', 'last_name', 'email', 'mobile']
    readonly_fields = ['customer_id', 'created_at', 'updated_at']
""",
    r"crm_project\brands\__init__.py": "",
    r"crm_project\brands\apps.py": """from django.apps import AppConfig
class BrandsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'brands'
    verbose_name = 'Brands'
""",
    r"crm_project\brands\models.py": """from django.db import models
from core.models import TimeStampedModel

class Brand(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='brands/logos/', blank=True, null=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    contact_info = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
""",
    r"crm_project\brands\views.py": """from django.shortcuts import render
from .models import Brand
def brand_list(request):
    brands = Brand.objects.filter(is_active=True)
    return render(request, 'brands/list.html', {'brands': brands})
""",
    r"crm_project\brands\urls.py": """from django.urls import path
from . import views
app_name = 'brands'
urlpatterns = [
    path('', views.brand_list, name='list'),
]
""",
    r"crm_project\brands\admin.py": """from django.contrib import admin
from .models import Brand
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
""",
    r"crm_project\categories\__init__.py": "",
    r"crm_project\categories\apps.py": """from django.apps import AppConfig
class CategoriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'categories'
    verbose_name = 'Categories'
""",
    r"crm_project\categories\models.py": """from django.db import models
from core.models import TimeStampedModel

class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        if self.parent:
            return f'{self.parent.name} > {self.name}'
        return self.name

    @property
    def is_root(self):
        return self.parent is None
""",
    r"crm_project\categories\views.py": """from django.shortcuts import render
from .models import Category
def category_list(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'categories/list.html', {'categories': categories})
""",
    r"crm_project\categories\urls.py": """from django.urls import path
from . import views
app_name = 'categories'
urlpatterns = [
    path('', views.category_list, name='list'),
]
""",
    r"crm_project\categories\admin.py": """from django.contrib import admin
from .models import Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'parent']
""",
    r"crm_project\products\__init__.py": "",
    r"crm_project\products\apps.py": """from django.apps import AppConfig
class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    verbose_name = 'Products'
""",
    r"crm_project\products\models.py": """from django.db import models
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
""",
    r"crm_project\products\views.py": """from django.shortcuts import render
from .models import Product
def product_list(request):
    products = Product.objects.filter(is_deleted=False).select_related('brand', 'category')
    return render(request, 'products/list.html', {'products': products})
""",
    r"crm_project\products\urls.py": """from django.urls import path
from . import views
app_name = 'products'
urlpatterns = [
    path('', views.product_list, name='list'),
]
""",
    r"crm_project\products\admin.py": """from django.contrib import admin
from .models import Product, ProductImage, ProductSpecification, SerialNumber

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSpecInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'brand', 'category', 'selling_price', 'status']
    inlines = [ProductImageInline, ProductSpecInline]

@admin.register(SerialNumber)
class SerialNumberAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'product', 'customer', 'status']
"""
}

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

for path, content in files.items():
    write_file(path, content)

print("Files created successfully.")
