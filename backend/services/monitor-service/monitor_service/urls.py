from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from apps.dashboard.views import DashboardView
from apps.monitoring import MonitorMetricsView, MonitorControlView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/monitor/stats/', DashboardView.as_view(), name='dashboard_stats'),
    path('api/v1/monitor/metrics/', MonitorMetricsView.as_view(), name='monitor_metrics'),
    path('api/v1/monitor/control/', MonitorControlView.as_view(), name='monitor_control'),
    path('api/v1/health/', lambda request: JsonResponse({"status": "online", "db_status": "connected", "cpu_percent": 1, "memory_percent": 20}), name='health'),
    path('api/v1/config/', include('apps.config_manager.urls')),
    path('api/v1/monitor/', include('apps.dashboard.urls')), # Keep legacy if needed, or remove if duplicates
]
