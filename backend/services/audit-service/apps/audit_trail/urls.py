from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuditLogViewSet, HealthCheckView
from apps.common.monitoring import MonitorMetricsView, MonitorControlView

router = DefaultRouter()
router.register(r'logs', AuditLogViewSet, basename='audit-logs')

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health_check'),
    # Monitoring
    path('monitor/metrics/', MonitorMetricsView.as_view(), name='monitor_metrics'),
    path('monitor/control/', MonitorControlView.as_view(), name='monitor_control'),
    path('', include(router.urls)),
]
