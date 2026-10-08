from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('access', 'Access'),
        ('assign', 'Assign'),
        ('status_change', 'Status Change'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='audit_logs'
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    object_id = models.CharField(max_length=50, blank=True)
    object_repr = models.CharField(max_length=200, blank=True)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user']),
            models.Index(fields=['action']),
        ]

    def __str__(self):
        return f'{self.user} — {self.action} — {self.object_repr}'


def log_action(user, action, obj=None, old_value=None, new_value=None,
               ip_address=None, user_agent=''):
    """Utility to create an audit log entry."""
    kwargs = {
        'user': user,
        'action': action,
        'old_value': old_value,
        'new_value': new_value,
        'ip_address': ip_address,
        'user_agent': user_agent,
    }
    if obj:
        ct = ContentType.objects.get_for_model(obj)
        kwargs['content_type'] = ct
        kwargs['object_id'] = str(obj.pk)
        kwargs['object_repr'] = str(obj)[:200]
    AuditLog.objects.create(**kwargs)

