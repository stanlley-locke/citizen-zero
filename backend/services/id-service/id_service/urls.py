from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from apps.common.monitoring import MonitorMetricsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ping/', lambda request: JsonResponse({"status": "ok"}), name='ping'),
    path('api/v1/monitor/metrics/', MonitorMetricsView.as_view(), name='metrics'),
    path('api/v1/', include('apps.digital_id.urls')),
]
