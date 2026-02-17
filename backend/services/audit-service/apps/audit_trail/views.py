from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.AllowAny] # For MVP/Local Dev

    def get_queryset(self):
        queryset = self.queryset
        
        # Filtering
        user_id = self.request.query_params.get('user_id')
        severity = self.request.query_params.get('severity')
        action = self.request.query_params.get('action')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if user_id:
            queryset = queryset.filter(user_id__icontains=user_id)
        if severity:
            queryset = queryset.filter(severity=severity)
        if action:
            queryset = queryset.filter(action=action)
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
            
        return queryset

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """
        Returns stats for Security Dashboard Overview.
        """
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Count
        
        now = timezone.now()
        last_24h = now - timedelta(hours=24)
        
        # 1. KPI Stats
        total_24h = self.queryset.filter(timestamp__gte=last_24h).count()
        errors_24h = self.queryset.filter(timestamp__gte=last_24h, status__in=['ERROR', 'FAILURE']).count()
        threats_active = self.queryset.filter(severity='CRITICAL', timestamp__gte=last_24h).count()
        
        # 2. Activity Trends (Mocking slightly since proper time-series aggregation in SQLite is tricky without complex annotations)
        # In prod (Postgres), we'd use TruncHour.
        
        # 3. Top Actions
        top_actions = self.queryset.filter(timestamp__gte=last_24h).values('action').annotate(count=Count('action')).order_by('-count')[:5]

        return Response({
            "kpi": {
                "active_threats": threats_active,
                "failed_attempts": errors_24h,
                "total_events": total_24h,
                "security_score": max(100 - (threats_active * 10) - (errors_24h), 0) # Mock Score
            },
            "activity": {
                "labels": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
                "data": [12, 19, 3, 5, 2, 3] # Mock distribution for now
            },
            "top_actions": top_actions
        })

    @action(detail=False, methods=['get'])
    def alerts(self, request):
        """
        Custom endpoint to fetch alerts (WARNING and CRITICAL severity).
        Defaults to last 24 hours if no date range provided.
        """
        from django.utils import timezone
        from datetime import timedelta
        
        # Default to last 24h
        cutoff = timezone.now() - timedelta(hours=24)
        
        queryset = self.queryset.filter(
            severity__in=['WARNING', 'CRITICAL'],
            timestamp__gte=cutoff
        ).order_by('-timestamp')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

from rest_framework.views import APIView
from django.db import connection
import psutil
import os
import time

class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = []

    def get(self, request):
        cpu_usage = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()
        process = psutil.Process(os.getpid())
        uptime = time.time() - process.create_time()
        
        db_status = "disconnected"
        try:
            connection.ensure_connection()
            db_status = "connected"
        except Exception:
            db_status = "error"

        return Response({
            "service": "audit-service",
            "status": "active" if db_status == "connected" else "degraded",
            "cpu_percent": cpu_usage,
            "memory_percent": memory.percent,
            "memory_used_mb": int(memory.used / 1024 / 1024),
            "uptime_seconds": int(uptime),
            "db_status": db_status
        })
