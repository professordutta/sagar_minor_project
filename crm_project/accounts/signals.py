from django.db.models.signals import post_save
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
