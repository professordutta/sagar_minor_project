from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to require specific user roles."""
    allowed_roles = []  # List of role names (group names)

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if not self.allowed_roles:
            return True
        return user.groups.filter(name__in=self.allowed_roles).exists()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied


class CustomerAccessMixin(LoginRequiredMixin):
    """Mixin for customer-only views. Ensures customers access only their own data."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not hasattr(request.user, 'customer_profile'):
            messages.error(request, 'Customer profile not found.')
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)


class StaffRequiredMixin(RoleRequiredMixin):
    """Requires the user to be staff (any non-customer role)."""
    allowed_roles = ['super_admin', 'crm_staff', 'service_agent', 'sales_staff', 'technician']


class AdminRequiredMixin(RoleRequiredMixin):
    """Requires super_admin or crm_staff."""
    allowed_roles = ['super_admin', 'crm_staff']


class SuperAdminMixin(RoleRequiredMixin):
    """Requires super_admin."""
    allowed_roles = ['super_admin']
