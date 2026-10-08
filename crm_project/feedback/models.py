from django.db import models
from core.models import TimeStampedModel


class Feedback(TimeStampedModel):
    RATING_CHOICES = [
        (1, '1 — Very Poor'),
        (2, '2 — Poor'),
        (3, '3 — Average'),
        (4, '4 — Good'),
        (5, '5 — Excellent'),
    ]

    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.CASCADE, related_name='feedbacks'
    )
    complaint = models.OneToOneField(
        'complaints.Complaint', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='feedback'
    )
    service_request = models.OneToOneField(
        'service.ServiceRequest', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='feedback'
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comments = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.customer.full_name} — {self.rating}/5'

