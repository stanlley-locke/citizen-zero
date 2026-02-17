from django.contrib import admin
from django.urls import path, include
from apps.monitoring import MonitorMetricsView, MonitorControlView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/citizens/', include('apps.citizens.urls')),
    path('api/v1/monitor/metrics/', MonitorMetricsView.as_view(), name='monitor-metrics'),
    path('api/v1/monitor/control/', MonitorControlView.as_view(), name='monitor-control'),
]
