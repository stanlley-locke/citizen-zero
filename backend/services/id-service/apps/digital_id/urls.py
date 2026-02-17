from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, DigitalIDViewSet, IssuanceRequestViewSet, CitizenProxyViewSet, health_check

router = DefaultRouter()
router.register(r'digital_ids', DigitalIDViewSet, basename='digital_ids')
router.register(r'requests', IssuanceRequestViewSet, basename='requests')
router.register(r'documents', DocumentViewSet, basename='documents')
router.register(r'citizens', CitizenProxyViewSet, basename='citizens')

urlpatterns = [
    path('health/', health_check, name='health'),
    path('', include(router.urls)),
]
