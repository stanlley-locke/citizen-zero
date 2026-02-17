from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class VerifyTokenView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'token required'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Stub logic: Online verification would call ID Service or check signature
        # For Mock MVP, assume valid if it starts with "valid_"
        is_valid = token.startswith("valid_") or True # Default true for demo
        
        # Log to Audit Service
        from apps.audit.services import AuditLogger
        
        # In a real scenario, the token would contain the User ID being verified.
        # For this mock, let's extract or pretend.
        # Also request should probably denote WHO is verifying.
        verifier_name = request.data.get('verifier_name', 'Third Party App')
        subject_id = request.data.get('user_id', 'Unknown Subject')
        
        AuditLogger.log(
            action='VERIFY_ID',
            user_id=subject_id, # The person being verified
            username=verifier_name, # The verifier entity
            actor_type='SYSTEM', # Or 'VERIFIER' if we add that choice
            details=f"ID Verification by {verifier_name}",
            status='SUCCESS' if is_valid else 'FAILURE',
            severity='INFO'
        )
        
        return Response({
            'valid': is_valid,
            'status': 'verified',
            'issuer': 'CitizenZero ID Authority'
        })

from django.db import connection
import psutil
import os
import time

class HealthCheckView(APIView):
    permission_classes = []
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
            "service": "verify-service",
            "status": "active" if db_status == "connected" else "degraded",
            "cpu_percent": cpu_usage,
            "memory_percent": memory.percent,
            "memory_used_mb": int(memory.used / 1024 / 1024),
            "uptime_seconds": int(uptime),
            "db_status": db_status
        })
