from django.urls import path
from .views import DashboardView, TriggerBackupView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('backup/', TriggerBackupView.as_view(), name='trigger_backup'),
]
