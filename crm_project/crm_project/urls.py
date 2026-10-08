from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('customers/', include('customers.urls', namespace='customers')),
    path('brands/', include('brands.urls', namespace='brands')),
    path('categories/', include('categories.urls', namespace='categories')),
    path('products/', include('products.urls', namespace='products')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('warranties/', include('warranties.urls', namespace='warranties')),
    path('complaints/', include('complaints.urls', namespace='complaints')),
    path('service/', include('service.urls', namespace='service')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('feedback/', include('feedback.urls', namespace='feedback')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('audit/', include('audit.urls', namespace='audit')),
    path('api/v1/', include('core.api_urls', namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'core.views.error_400'
handler403 = 'core.views.error_403'
handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'
