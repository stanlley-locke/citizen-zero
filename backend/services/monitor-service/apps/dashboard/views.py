from rest_framework.views import APIView
from rest_framework.response import Response
from .apps import store, BackupManager
import time
from django.conf import settings

class DashboardView(APIView):
    def get(self, request):
        total_services = len(settings.MONITORED_SERVICES)
        online_services = sum(1 for s in store.services.values() if s.get('status') == 'online')
        
        nodes = []
        for svc in settings.MONITORED_SERVICES:
            name = svc['name']
            current = store.services.get(name, {})
            node = {
                "id": name,
                "label": name,
                "service": name, # Explicit service name for frontend mapping
                "status": current.get('status', 'offline'),
                "latency": current.get('latency', 0),
                "db_status": current.get('database', {}).get('status', 'unknown'),
                "cpu_percent": current.get('resources', {}).get('cpu', 0),
                "memory_percent": current.get('resources', {}).get('memory', 0),
                "metrics": current.get('metrics', {}),
                "resources": current.get('resources', {}),
                "database": current.get('database', {}),
                "backup": current.get('backup', {})
            }
            nodes.append(node)
            
        return Response({
            "summary": {
                "total": total_services,
                "online": online_services,
                "healthy_percentage": int((online_services/total_services)*100) if total_services > 0 else 0
            },
            "nodes": nodes,
            "updated_at": time.time()
        })

class TriggerBackupView(APIView):
    def post(self, request):
        service_name = request.data.get('service_name')
        if not service_name:
            return Response({"error": "service_name required"}, status=400)
            
        success, msg = BackupManager.create_snapshot(service_name)
        return Response({"success": success, "message": msg})
