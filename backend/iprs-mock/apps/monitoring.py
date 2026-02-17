from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.deprecation import MiddlewareMixin
from collections import deque
from django.http import JsonResponse
import time
import json

# --- Singleton Store (In-Memory) ---
class ServiceState:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServiceState, cls).__new__(cls)
            cls._instance.requests = deque(maxlen=50) # Keep last 50 requests
            cls._instance.maintenance_mode = False
            cls._instance.total_requests = 0
            cls._instance.error_count = 0
        return cls._instance

state = ServiceState()

# --- Middleware ---
class TrafficControlMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if state.maintenance_mode:
            # Bypass for admin or control endpoints to allow disabling
            if "/monitor/control/" in request.path:
                return None
            return JsonResponse({"error": "Service in Maintenance Mode"}, status=503)

    def process_response(self, request, response):
        if "/monitor/" in request.path:
            return response
            
        # Log Traffic
        latency = 0 # Calculate if needed, simplified
        
        log_entry = {
            "timestamp": time.time(),
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "ip": request.META.get('REMOTE_ADDR'),
            "client": request.META.get('HTTP_USER_AGENT', 'unknown')[:30]
        }
        
        state.requests.append(log_entry)
        state.total_requests += 1
        if response.status_code >= 400:
            state.error_count += 1
            
        return response

# --- Views ---
class MonitorMetricsView(APIView):
    permission_classes = []
    throttle_classes = [] 

    def get(self, request):
        return Response({
            "maintenance_mode": state.maintenance_mode,
            "total_requests": state.total_requests,
            "error_count": state.error_count,
            "recent_traffic": list(state.requests)
        })

class MonitorControlView(APIView):
    permission_classes = [] # In prod, secure this!
    throttle_classes = []

    def post(self, request):
        mode = request.data.get('maintenance_mode')
        if mode is not None:
            state.maintenance_mode = bool(mode)
        
        # Reset counters action
        if request.data.get('reset_counters'):
            state.total_requests = 0
            state.error_count = 0
            state.requests.clear()

        return Response({
            "status": "updated",
            "maintenance_mode": state.maintenance_mode
        })
