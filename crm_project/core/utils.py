import random
import string
from datetime import date
from django.utils import timezone


def generate_unique_id(prefix, model_class, field_name, length=6):
    """Generate a unique ID like TKT-2026-000001."""
    year = timezone.now().year
    while True:
        number = ''.join(random.choices(string.digits, k=length))
        uid = f"{prefix}-{year}-{number}"
        if not model_class.objects.filter(**{field_name: uid}).exists():
            return uid


def get_warranty_status(warranty_end_date):
    """Calculate warranty status from end date."""
    today = date.today()
    if warranty_end_date < today:
        return 'expired'
    days_remaining = (warranty_end_date - today).days
    if days_remaining <= 30:
        return 'expiring_soon'
    return 'active'


def get_warranty_display(warranty_end_date):
    """Get human-readable warranty status."""
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
