from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, UserStatsView, AdminLoginView, UserListView, AdminUserViewSet, HealthCheckView
from apps.common.monitoring import MonitorMetricsView, MonitorControlView

router = DefaultRouter()
router.register(r'admin/users', AdminUserViewSet, basename='admin-users')

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/stats/', UserStatsView.as_view(), name='user_stats'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    path('health/', HealthCheckView.as_view(), name='health_check'),
    # Monitoring
    path('monitor/metrics/', MonitorMetricsView.as_view(), name='monitor_metrics'),
    path('monitor/control/', MonitorControlView.as_view(), name='monitor_control'),
    path('', include(router.urls)),
]
