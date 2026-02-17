from django.urls import path
from .views import VerifyTokenView, HealthCheckView
from apps.common.monitoring import MonitorMetricsView, MonitorControlView

urlpatterns = [
    path('token/', VerifyTokenView.as_view(), name='verify_token'),
    path('health/', HealthCheckView.as_view(), name='health_check'),
    # Monitoring
    path('monitor/metrics/', MonitorMetricsView.as_view(), name='monitor_metrics'),
    path('monitor/control/', MonitorControlView.as_view(), name='monitor_control'),
]
