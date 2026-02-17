from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ping/', lambda request: JsonResponse({"status": "ok"}), name='ping'),
    path('api/v1/audit/', include('apps.audit_trail.urls')),
]
