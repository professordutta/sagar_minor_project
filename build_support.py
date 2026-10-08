import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

base_dir = "d:/sagar_minor_project/crm_project"

# ----------------- ACCOUNTS -----------------

accounts_views = """from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', user.get_dashboard_url())
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html', {})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def change_password_view(request):
    from django.contrib.auth.forms import PasswordChangeForm
    from django.contrib.auth import update_session_auth_hash
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
"""

accounts_urls = """from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
]
"""

profile_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="bg-white shadow rounded-lg p-6 max-w-2xl mx-auto">
    <h1 class="text-2xl font-bold mb-6">My Profile</h1>
    <div class="grid grid-cols-2 gap-4">
        <div><strong>Name:</strong> {{ user.full_name }}</div>
        <div><strong>Email:</strong> {{ user.email }}</div>
        <div><strong>Mobile:</strong> {{ user.mobile|default:"-" }}</div>
        <div><strong>Role:</strong> {{ user.primary_role|title|default:"User" }}</div>
    </div>
    <div class="mt-6 border-t pt-6">
        <a href="{% url 'accounts:change_password' %}" class="text-indigo-600 hover:text-indigo-900">Change Password</a>
    </div>
</div>
{% endblock %}
"""

change_password_html = """{% extends 'dashboard/base.html' %}
{% load crispy_forms_tags %}
{% block content %}
<div class="bg-white shadow rounded-lg p-6 max-w-2xl mx-auto">
    <h1 class="text-2xl font-bold mb-6">Change Password</h1>
    <form method="post">
        {% csrf_token %}
        {{ form|crispy }}
        <div class="mt-6 flex justify-end gap-4">
            <a href="{% url 'accounts:profile' %}" class="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300">Cancel</a>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Change Password</button>
        </div>
    </form>
</div>
{% endblock %}
"""

# ----------------- DASHBOARD -----------------
dashboard_urls = """from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('service-agent/', views.service_agent_dashboard, name='service_agent_dashboard'),
    path('sales/', views.sales_dashboard, name='sales_dashboard'),
    path('technician/', views.technician_dashboard, name='technician_dashboard'),
]
"""

customer_dashboard_html = """{% extends 'dashboard/base.html' %}
{% block title %}My Dashboard{% endblock %}
{% block content %}
<div class="mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Welcome, {{ request.user.first_name }}!</h1>
</div>
<div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
    <div class="bg-white rounded-lg shadow p-6 border-t-4 border-blue-500">
        <h3 class="text-sm font-medium text-gray-500">My Orders</h3>
        <p class="text-2xl font-bold text-gray-900">{{ orders_count|default:"0" }}</p>
    </div>
    <div class="bg-white rounded-lg shadow p-6 border-t-4 border-green-500">
        <h3 class="text-sm font-medium text-gray-500">Active Warranties</h3>
        <p class="text-2xl font-bold text-gray-900">{{ active_warranties_count|default:"0" }}</p>
    </div>
</div>
{% endblock %}
"""

service_agent_html = """{% extends 'dashboard/base.html' %}
{% block title %}Service Agent Dashboard{% endblock %}
{% block content %}
<div class="mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Service Agent Dashboard</h1>
</div>
<div class="bg-white rounded-lg shadow p-6">
    <h3 class="text-lg font-medium text-gray-900 mb-4">Assigned Complaints ({{ assigned_count }})</h3>
    <ul class="divide-y divide-gray-200">
        {% for c in assigned_complaints %}
        <li class="py-3 flex justify-between">
            <span><a href="{% url 'complaints:detail' c.pk %}" class="text-blue-600 hover:underline">{{ c.ticket_id }}</a> - {{ c.customer.full_name }}</span>
            <span class="text-sm text-gray-500">{{ c.get_status_display }}</span>
        </li>
        {% empty %}
        <li class="py-3 text-gray-500 text-sm">No assigned complaints.</li>
        {% endfor %}
    </ul>
</div>
{% endblock %}
"""

sales_html = """{% extends 'dashboard/base.html' %}
{% block title %}Sales Dashboard{% endblock %}
{% block content %}
<div class="mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Sales Dashboard</h1>
</div>
<div class="bg-white rounded-lg shadow p-6">
    <h3 class="text-lg font-medium text-gray-900 mb-4">Recent Orders ({{ my_orders_count }} total)</h3>
    <ul class="divide-y divide-gray-200">
        {% for o in recent_orders %}
        <li class="py-3 flex justify-between">
            <span><a href="{% url 'orders:detail' o.pk %}" class="text-blue-600 hover:underline">{{ o.order_number }}</a> - {{ o.customer.full_name }}</span>
            <span class="text-sm font-semibold text-gray-700">₹{{ o.grand_total }}</span>
        </li>
        {% empty %}
        <li class="py-3 text-gray-500 text-sm">No recent orders.</li>
        {% endfor %}
    </ul>
</div>
{% endblock %}
"""

technician_html = """{% extends 'dashboard/base.html' %}
{% block title %}Technician Dashboard{% endblock %}
{% block content %}
<div class="mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Technician Dashboard</h1>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
    <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Today's Visits ({{ today_count }})</h3>
        <ul class="divide-y divide-gray-200">
            {% for j in today_visits %}
            <li class="py-3 flex justify-between">
                <span><a href="{% url 'service:detail' j.pk %}" class="text-blue-600 hover:underline">{{ j.service_id }}</a> - {{ j.customer.full_name }}</span>
            </li>
            {% empty %}
            <li class="py-3 text-gray-500 text-sm">No visits scheduled for today.</li>
            {% endfor %}
        </ul>
    </div>
    <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">All Open Jobs ({{ open_jobs_count }})</h3>
        <ul class="divide-y divide-gray-200">
            {% for j in my_jobs %}
            <li class="py-3 flex justify-between">
                <span><a href="{% url 'service:detail' j.pk %}" class="text-blue-600 hover:underline">{{ j.service_id }}</a></span>
                <span class="text-sm text-gray-500">{{ j.scheduled_date|date:"M d, Y" }}</span>
            </li>
            {% empty %}
            <li class="py-3 text-gray-500 text-sm">No open jobs.</li>
            {% endfor %}
        </ul>
    </div>
</div>
{% endblock %}
"""

# ----------------- NOTIFICATIONS -----------------
notifications_urls = """from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('<int:pk>/read/', views.mark_read, name='mark_read'),
]
"""

notifications_views = """from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

@login_required
def mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications:list')
"""

notifications_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="bg-white shadow rounded-lg overflow-hidden max-w-4xl mx-auto">
    <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-xl font-bold">Notifications</h2>
    </div>
    <ul class="divide-y divide-gray-200">
        {% for n in notifications %}
        <li class="p-4 {% if not n.is_read %}bg-blue-50{% endif %} flex justify-between items-center">
            <div>
                <p class="font-medium text-gray-900">{{ n.title }}</p>
                <p class="text-sm text-gray-500">{{ n.message }}</p>
                <p class="text-xs text-gray-400 mt-1">{{ n.created_at|timesince }} ago</p>
            </div>
            {% if not n.is_read %}
            <a href="{% url 'notifications:mark_read' n.pk %}" class="text-sm text-blue-600 hover:underline">Mark read</a>
            {% endif %}
        </li>
        {% empty %}
        <li class="p-4 text-center text-gray-500">No notifications.</li>
        {% endfor %}
    </ul>
</div>
{% endblock %}
"""

# ----------------- FEEDBACK -----------------
feedback_urls = """from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.feedback_list, name='list'),
    path('add/', views.feedback_create, name='create'),
]
"""

feedback_views = """from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback
from .forms import FeedbackForm

@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.select_related('customer', 'order').order_by('-created_at')
    return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks})

@login_required
def feedback_create(request):
    from customers.models import Customer
    customer = getattr(request.user, 'customer_profile', None)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            if customer:
                fb.customer = customer
            fb.save()
            return redirect('feedback:list')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback_form.html', {'form': form})
"""

feedback_forms = """from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['order', 'product', 'rating', 'comments']
"""

feedback_list_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Feedback</h1>
    <a href="{% url 'feedback:create' %}" class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700">Add Feedback</a>
</div>
<div class="bg-white shadow rounded-lg overflow-hidden">
    <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Customer</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rating</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Comments</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            {% for fb in feedbacks %}
            <tr>
                <td class="px-6 py-4 whitespace-nowrap">{{ fb.customer|default:"Anonymous" }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ fb.rating }}/5</td>
                <td class="px-6 py-4">{{ fb.comments|truncatechars:50 }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ fb.created_at|date:"M d, Y" }}</td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4" class="px-6 py-4 text-center text-gray-500">No feedback found.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
"""

feedback_form_html = """{% extends 'dashboard/base.html' %}
{% load crispy_forms_tags %}
{% block content %}
<div class="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow">
    <h1 class="text-2xl font-bold mb-6">Submit Feedback</h1>
    <form method="post">
        {% csrf_token %}
        {{ form|crispy }}
        <div class="mt-6 flex justify-end gap-4">
            <a href="{% url 'feedback:list' %}" class="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300">Cancel</a>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Submit</button>
        </div>
    </form>
</div>
{% endblock %}
"""

# ----------------- AUDIT -----------------
audit_urls = """from django.urls import path
from . import views

app_name = 'audit'

urlpatterns = [
    path('', views.audit_log_list, name='list'),
]
"""

audit_views = """from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AuditLog

@login_required
def audit_log_list(request):
    logs = AuditLog.objects.select_related('user').order_by('-created_at')[:200]
    return render(request, 'audit/audit_list.html', {'logs': logs})
"""

audit_list_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Audit Logs</h1>
</div>
<div class="bg-white shadow rounded-lg overflow-hidden">
    <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Action</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Model</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">IP Address</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Timestamp</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200 text-sm">
            {% for log in logs %}
            <tr>
                <td class="px-6 py-3 whitespace-nowrap">{{ log.user|default:"System" }}</td>
                <td class="px-6 py-3 whitespace-nowrap">{{ log.get_action_display }}</td>
                <td class="px-6 py-3 whitespace-nowrap">{{ log.model_name }} ({{ log.object_id }})</td>
                <td class="px-6 py-3 whitespace-nowrap">{{ log.ip_address|default:"-" }}</td>
                <td class="px-6 py-3 whitespace-nowrap">{{ log.created_at|date:"M d, Y H:i:s" }}</td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">No audit logs found.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
"""

audit_middleware = """class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
"""

# ----------------- REPORTS -----------------
reports_urls = """from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_home, name='home'),
]
"""

reports_views = """from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def reports_home(request):
    return render(request, 'reports/reports_home.html', {})
"""

reports_home_html = """{% extends 'dashboard/base.html' %}
{% block content %}
<div class="bg-white shadow rounded-lg p-10 text-center">
    <i class="fas fa-chart-bar text-6xl text-gray-300 mb-4"></i>
    <h1 class="text-2xl font-bold text-gray-800">Reports Module</h1>
    <p class="text-gray-500 mt-2">The reporting engine is currently under development. Please check back later.</p>
</div>
{% endblock %}
"""

# ----------------- CORE -----------------
api_urls = """from django.urls import path
app_name = 'api'
urlpatterns = []
"""

core_context = """def global_context(request):
    return {
        'app_name': 'Vijay CRM',
    }
"""

notifications_context = """def notifications_context(request):
    if request.user.is_authenticated:
        from .models import Notification
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return {'unread_notifications_count': count}
    return {'unread_notifications_count': 0}
"""

# Execute writes
write_file(f"{base_dir}/accounts/views.py", accounts_views)
write_file(f"{base_dir}/accounts/urls.py", accounts_urls)
write_file(f"{base_dir}/templates/accounts/profile.html", profile_html)
write_file(f"{base_dir}/templates/accounts/change_password.html", change_password_html)

write_file(f"{base_dir}/dashboard/urls.py", dashboard_urls)
write_file(f"{base_dir}/templates/dashboard/customer.html", customer_dashboard_html)
write_file(f"{base_dir}/templates/dashboard/service_agent.html", service_agent_html)
write_file(f"{base_dir}/templates/dashboard/sales.html", sales_html)
write_file(f"{base_dir}/templates/dashboard/technician.html", technician_html)

write_file(f"{base_dir}/notifications/urls.py", notifications_urls)
write_file(f"{base_dir}/notifications/views.py", notifications_views)
write_file(f"{base_dir}/templates/notifications/notification_list.html", notifications_html)
write_file(f"{base_dir}/notifications/context_processors.py", notifications_context)

write_file(f"{base_dir}/feedback/urls.py", feedback_urls)
write_file(f"{base_dir}/feedback/views.py", feedback_views)
write_file(f"{base_dir}/feedback/forms.py", feedback_forms)
write_file(f"{base_dir}/templates/feedback/feedback_list.html", feedback_list_html)
write_file(f"{base_dir}/templates/feedback/feedback_form.html", feedback_form_html)

write_file(f"{base_dir}/audit/urls.py", audit_urls)
write_file(f"{base_dir}/audit/views.py", audit_views)
write_file(f"{base_dir}/templates/audit/audit_list.html", audit_list_html)
write_file(f"{base_dir}/audit/middleware.py", audit_middleware)

write_file(f"{base_dir}/reports/urls.py", reports_urls)
write_file(f"{base_dir}/reports/views.py", reports_views)
write_file(f"{base_dir}/templates/reports/reports_home.html", reports_home_html)

write_file(f"{base_dir}/core/api_urls.py", api_urls)
write_file(f"{base_dir}/core/context_processors.py", core_context)

print("Support modules generated.")

