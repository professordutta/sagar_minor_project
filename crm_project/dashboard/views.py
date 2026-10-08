from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Sum
from datetime import timedelta


@login_required
def home(request):
    """Main dashboard redirect based on role."""
    user = request.user
    if user.is_superuser or user.has_role('super_admin', 'crm_staff'):
        return redirect('dashboard:admin_dashboard')
    elif user.has_role('service_agent'):
        return redirect('dashboard:service_agent_dashboard')
    elif user.has_role('sales_staff'):
        return redirect('dashboard:sales_dashboard')
    elif user.has_role('technician'):
        return redirect('dashboard:technician_dashboard')
    elif user.has_role('customer'):
        return redirect('dashboard:customer_dashboard')
    return redirect('dashboard:admin_dashboard')


@login_required
def admin_dashboard(request):
    """Admin/CRM staff dashboard."""
    from customers.models import Customer
    from orders.models import Order
    from complaints.models import Complaint
    from warranties.models import Warranty
    from service.models import ServiceRequest
    from feedback.models import Feedback
    from django.db.models import Avg

    today = timezone.now().date()
    last_30 = today - timedelta(days=30)

    # KPIs
    total_customers = Customer.objects.filter(is_deleted=False).count()
    new_customers_month = Customer.objects.filter(created_at__date__gte=last_30, is_deleted=False).count()
    total_orders = Order.objects.filter(is_deleted=False).count()
    orders_value = Order.objects.filter(is_deleted=False, order_status='delivered').aggregate(total=Sum('grand_total'))['total'] or 0
    open_complaints = Complaint.objects.filter(status__in=['open','assigned','in_progress'], is_deleted=False).count()
    critical_complaints = Complaint.objects.filter(priority='critical', status__in=['open','assigned','in_progress'], is_deleted=False).count()
    pending_services = ServiceRequest.objects.filter(status__in=['requested','scheduled','technician_assigned']).count()
    active_warranties = Warranty.objects.filter(status='active').count()
    expiring_warranties = Warranty.objects.filter(status='expiring_soon').count()
    sla_breaches = Complaint.objects.filter(sla_breach=True, is_deleted=False).count()
    avg_rating = Feedback.objects.aggregate(avg=Avg('rating'))['avg']
    csat = round(avg_rating * 20, 1) if avg_rating else 0  # Convert 5-star to 100%

    # Recent activity
    recent_complaints = Complaint.objects.filter(is_deleted=False).select_related('customer').order_by('-created_at')[:5]
    recent_orders = Order.objects.filter(is_deleted=False).select_related('customer').order_by('-created_at')[:5]
    recent_customers = Customer.objects.filter(is_deleted=False).order_by('-created_at')[:5]

    # Chart data — complaints by category (last 30 days)
    complaint_categories = (
        Complaint.objects.filter(is_deleted=False, created_at__date__gte=last_30)
        .values('category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Chart data — daily new customers last 7 days
    customer_trend = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        count = Customer.objects.filter(created_at__date=d, is_deleted=False).count()
        customer_trend.append({'date': d.strftime('%d %b'), 'count': count})

    context = {
        'total_customers': total_customers,
        'new_customers_month': new_customers_month,
        'total_orders': total_orders,
        'orders_value': orders_value,
        'open_complaints': open_complaints,
        'critical_complaints': critical_complaints,
        'pending_services': pending_services,
        'active_warranties': active_warranties,
        'expiring_warranties': expiring_warranties,
        'sla_breaches': sla_breaches,
        'csat': csat,
        'avg_rating': avg_rating,
        'recent_complaints': recent_complaints,
        'recent_orders': recent_orders,
        'recent_customers': recent_customers,
        'complaint_categories': list(complaint_categories),
        'customer_trend': customer_trend,
        'page_title': 'Admin Dashboard',
    }
    return render(request, 'dashboard/admin.html', context)


@login_required
def customer_dashboard(request):
    if not hasattr(request.user, 'customer_profile'):
        from django.contrib import messages
        messages.warning(request, 'No customer profile found.')
        return render(request, 'dashboard/customer.html', {'page_title': 'My Dashboard'})

    customer = request.user.customer_profile
    from orders.models import Order
    from warranties.models import Warranty
    from complaints.models import Complaint
    from service.models import ServiceRequest
    from notifications.models import Notification

    my_orders = Order.objects.filter(customer=customer, is_deleted=False).order_by('-created_at')[:5]
    my_warranties = Warranty.objects.filter(customer=customer, status__in=['active','expiring_soon']).select_related('product')[:5]
    my_complaints = Complaint.objects.filter(customer=customer, is_deleted=False, status__in=['open','assigned','in_progress']).order_by('-created_at')[:5]
    my_services = ServiceRequest.objects.filter(customer=customer, status__in=['requested','scheduled','technician_assigned']).order_by('-created_at')[:3]
    my_notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')[:10]

    context = {
        'customer': customer,
        'my_orders': my_orders,
        'my_warranties': my_warranties,
        'my_complaints': my_complaints,
        'my_services': my_services,
        'my_notifications': my_notifications,
        'orders_count': Order.objects.filter(customer=customer, is_deleted=False).count(),
        'active_warranties_count': Warranty.objects.filter(customer=customer, status='active').count(),
        'open_complaints_count': Complaint.objects.filter(customer=customer, is_deleted=False, status__in=['open','assigned','in_progress']).count(),
        'pending_services_count': ServiceRequest.objects.filter(customer=customer, status__in=['requested','scheduled']).count(),
        'page_title': 'My Dashboard',
    }
    return render(request, 'dashboard/customer.html', context)


@login_required
def service_agent_dashboard(request):
    from complaints.models import Complaint
    assigned = Complaint.objects.filter(
        assigned_to=request.user, is_deleted=False,
        status__in=['assigned','in_progress']
    ).select_related('customer').order_by('created_at')
    return render(request, 'dashboard/service_agent.html', {
        'assigned_complaints': assigned,
        'assigned_count': assigned.count(),
        'page_title': 'Service Agent Dashboard',
    })


@login_required
def sales_dashboard(request):
    from orders.models import Order
    recent_orders = Order.objects.filter(
        is_deleted=False, salesperson=request.user
    ).select_related('customer').order_by('-created_at')[:10]
    return render(request, 'dashboard/sales.html', {
        'recent_orders': recent_orders,
        'my_orders_count': Order.objects.filter(salesperson=request.user, is_deleted=False).count(),
        'page_title': 'Sales Dashboard',
    })


@login_required
def technician_dashboard(request):
    from service.models import ServiceRequest
    from django.utils import timezone
    today = timezone.now().date()
    my_jobs = ServiceRequest.objects.filter(
        technician=request.user,
        status__in=['technician_assigned','scheduled','repair_in_progress']
    ).select_related('customer', 'product').order_by('scheduled_date')
    today_visits = my_jobs.filter(scheduled_date__date=today)
    return render(request, 'dashboard/technician.html', {
        'my_jobs': my_jobs,
        'today_visits': today_visits,
        'today_count': today_visits.count(),
        'open_jobs_count': my_jobs.count(),
        'page_title': 'Technician Dashboard',
    })

