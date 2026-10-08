from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AuditLog

@login_required
def audit_log_list(request):
    logs = AuditLog.objects.select_related('user').order_by('-created_at')[:200]
    return render(request, 'audit/audit_list.html', {'logs': logs})
