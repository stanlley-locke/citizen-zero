from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Path for authentication URLs will be added later
    path('api/v1/auth/', include('apps.authentication.urls')),
]
