from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from customers.models import Customer
from brands.models import Brand
from categories.models import Category
from products.models import Product, SerialNumber
from orders.models import Order, OrderItem, Invoice
from warranties.models import Warranty
from complaints.models import Complaint, ComplaintActivity
from service.models import ServiceRequest
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data seed...')
        self.setup_users()
        self.setup_catalog()
        self.setup_customers_and_transactions()
        self.stdout.write(self.style.SUCCESS('Data seeding complete!'))

    def setup_users(self):
        self.stdout.write('Creating users...')
        users_data = [
            ('admin@example.com', 'Admin', 'User', 'super_admin', 'Admin@1234', True),
            ('crm@example.com', 'CRM', 'Staff', 'crm_staff', 'Crm@1234', False),
            ('agent@example.com', 'Service', 'Agent', 'service_agent', 'Agent@1234', False),
            ('technician@example.com', 'Tech', 'Guy', 'technician', 'Tech@1234', False),
            ('sales@example.com', 'Sales', 'Rep', 'sales_staff', 'Sales@1234', False),
            ('customer@example.com', 'Demo', 'Customer', 'customer', 'Customer@1234', False),
        ]

        for email, first, last, role, password, is_superuser in users_data:
            user, created = User.objects.get_or_create(email=email, defaults={
                'username': email.split('@')[0], 'first_name': first, 'last_name': last, 'is_staff': not (role == 'customer'),
                'is_superuser': is_superuser, 'mobile': f'99999{random.randint(10000,99999)}'
            })
            if created:
                user.set_password(password)
                user.save()
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

    def setup_catalog(self):
        self.stdout.write('Creating catalog...')
        brands = ['Samsung', 'LG', 'Sony', 'Apple', 'Bosch', 'Whirlpool']
        for b in brands:
            Brand.objects.get_or_create(name=b, defaults={'slug': b.lower()})
        
        categories = ['Televisions', 'Refrigerators', 'Washing Machines', 'Air Conditioners', 'Smartphones']
        for c in categories:
            Category.objects.get_or_create(name=c, defaults={'slug': c.lower().replace(' ', '-')})

        brand_objs = list(Brand.objects.all())
        cat_objs = list(Category.objects.all())

        for i in range(1, 21):
            Product.objects.get_or_create(
                sku=f'PRD-{i:04d}',
                defaults={
                    'name': f'Demo Product {i}',
                    'brand': random.choice(brand_objs),
                    'category': random.choice(cat_objs),
                    'mrp': random.randint(10000, 100000),
                    'selling_price': random.randint(8000, 95000),
                    'requires_serial_tracking': True,
                }
            )

    def setup_customers_and_transactions(self):
        self.stdout.write('Creating customers and transactions...')
        products = list(Product.objects.all())
        users = list(User.objects.filter(groups__name='customer'))
        staff = list(User.objects.filter(groups__name='crm_staff'))
        techs = list(User.objects.filter(groups__name='technician'))

        for user in users:
            customer, _ = Customer.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'mobile': user.mobile or f'99999{random.randint(10000,99999)}',
                    'city': 'Demo City'
                }
            )
            # Create Orders
            for _ in range(random.randint(1, 5)):
                order = Order.objects.create(
                    customer=customer,
                    grand_total=0,
                    order_status='delivered',
                    payment_status='paid'
                )
                total = 0
                for _ in range(random.randint(1, 3)):
                    prod = random.choice(products)
                    qty = 1
                    sn = SerialNumber.objects.create(
                        product=prod, serial_number=f'SN-{random.randint(100000,999999)}',
                        status='sold', customer=customer
                    )
                    price = prod.selling_price
                    total += price
                    OrderItem.objects.create(
                        order=order, product=prod, quantity=qty, unit_price=price,
                        total=price, serial_number=sn
                    )
                    
                    # Create Warranty
                    Warranty.objects.create(
                        customer=customer, product=prod, serial_number=sn,
                        purchase_date=timezone.now().date(),
                        warranty_start=timezone.now().date(),
                        warranty_end=(timezone.now() + timedelta(days=365)).date()
                    )
                
                order.grand_total = total
                order.subtotal = total
                order.save()
                
                Invoice.objects.create(
                    customer=customer, order=order, subtotal=total, grand_total=total, payment_status='paid'
                )

            # Create Complaints
            if random.random() > 0.5:
                comp = Complaint.objects.create(
                    customer=customer,
                    subject='Issue with product',
                    description='It stopped working suddenly.',
                    priority=random.choice(['low', 'medium', 'high', 'critical']),
                    status=random.choice(['open', 'assigned', 'in_progress']),
                    assigned_to=random.choice(staff) if staff else None
                )
                comp.set_sla_deadline()
                comp.save()
                
                # Service Request
                if random.random() > 0.5 and techs:
                    ServiceRequest.objects.create(
                        customer=customer,
                        complaint=comp,
                        technician=random.choice(techs),
                        status='scheduled',
                        scheduled_date=timezone.now() + timedelta(days=1)
                    )
