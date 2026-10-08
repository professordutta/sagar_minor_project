from django import template
from django.utils.safestring import mark_safe
from datetime import date

register = template.Library()

@register.filter
def status_badge(value, badge_type=None):
    """Render a colored status badge."""
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
    """Return 'active' class if current URL matches."""
    request = context.get('request')
    if request:
        for url in urls:
            if request.path.startswith(url):
                return 'active'
    return ''

@register.filter
def currency(value):
    """Format as Indian currency."""
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
