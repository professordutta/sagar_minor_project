from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from core.models import TimeStampedModel


class Notification(TimeStampedModel):
    TYPE_CHOICES = [
        ('order_confirmed', 'Order Confirmed'),
        ('order_delivered', 'Order Delivered'),
        ('warranty_activated', 'Warranty Activated'),
        ('warranty_expiring', 'Warranty Expiring'),
        ('complaint_created', 'Complaint Created'),
        ('complaint_assigned', 'Complaint Assigned'),
        ('complaint_updated', 'Complaint Updated'),
        ('service_scheduled', 'Service Scheduled'),
        ('service_completed', 'Service Completed'),
        ('invoice_generated', 'Invoice Generated'),
        ('general', 'General'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=30, choices=TYPE_CHOICES, default='general'
    )
    is_read = models.BooleanField(default=False, db_index=True)
    read_at = models.DateTimeField(null=True, blank=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    action_url = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'{self.title} → {self.recipient.email}'

    def mark_read(self):
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save(update_fields=['is_read', 'read_at'])


def send_notification(recipient, title, message, notification_type='general',
                      action_url='', related_object=None):
    """Utility function to create a notification."""
    kwargs = {
        'recipient': recipient,
        'title': title,
        'message': message,
        'notification_type': notification_type,
        'action_url': action_url,
    }
    if related_object:
        ct = ContentType.objects.get_for_model(related_object)
        kwargs['content_type'] = ct
        kwargs['object_id'] = related_object.pk
    return Notification.objects.create(**kwargs)

