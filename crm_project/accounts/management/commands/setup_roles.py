from django.core.management.base import BaseCommand
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
