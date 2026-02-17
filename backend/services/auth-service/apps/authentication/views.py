from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import LoginSerializer
from django.db import connection
import psutil
import os
import time

class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [] # Disable rate limiting for health check

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
            "service": "auth-service",
            "status": "active" if db_status == "connected" else "degraded",
            "cpu_percent": cpu_usage,
            "memory_percent": memory.percent,
            "memory_used_mb": int(memory.used / 1024 / 1024),
            "uptime_seconds": int(uptime),
            "db_status": db_status
        })

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = serializer.get_token(user)
            
            # Trigger Audit Log (Fire and Forget)
            try:
                import requests
                requests.post('http://127.0.0.1:8003/api/v1/audit/logs/', json={
                    'action': 'LOGIN',
                    'user_id': user.username, 
                    'username': user.username,
                    'actor_type': 'CITIZEN',
                    'details': f"User {user.username} logged in successfully",
                    'status': 'SUCCESS',
                    'ip_address': '127.0.0.1'
                }, timeout=1)
            except Exception as e:
                print(f"Audit Log Failed: {e}")

            return Response({
                'status': 'success',
                'tokens': tokens,
                'citizen': serializer.validated_data['citizen_data']
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import get_user_model

class UserStatsView(APIView):
    permission_classes = [AllowAny] # Ideally restricted to Admin

    def get(self, request):
        User = get_user_model()
        count = User.objects.count()
        return Response({'total_citizens': count}, status=status.HTTP_200_OK)

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        
        if user:
            # Enforce Portal Access (Any non-citizen role)
            # We no longer rely on is_staff, as that controls Django Admin Panel access.
            # We check the UserProfile role.
            
            allowed_roles = [
                'SYSTEM_ADMIN', 'ADMIN',
                'DATA_COLLECTOR', 'INVESTIGATOR',
                'DATA_CONTROLLER', 'DPO', 'ORG_ADMIN', 'HR_MANAGER', 'INT_AUDITOR', 'VERIFIER'
            ]
            
            # Check profile
            if hasattr(user, 'profile') and user.profile.role not in allowed_roles:
                 return Response({'error': 'Access denied. Authorized personnel only.'}, status=status.HTTP_403_FORBIDDEN)
            
            # Fallback for superusers without profile (shouldn't happen with updated signals/logic but safety net)
            if not hasattr(user, 'profile') and not user.is_superuser:
                 return Response({'error': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)
            
            # Trigger Audit Log
            try:
                import requests
                # Use a fire-and-forget timeout or background task in real prod
                requests.post('http://127.0.0.1:8003/api/v1/audit/logs/', json={
                    'action': 'ADMIN_LOGIN',
                    'user_id': user.username,
                    'username': user.username,
                    'actor_type': 'ADMIN',
                    'details': f"Admin {user.username} logged in via Desktop App",
                    'status': 'SUCCESS',
                    'ip_address': '127.0.0.1' 
                }, timeout=1)
            except Exception as e:
                print(f"Admin Audit Log Failed: {e}")

            # Ensure profile exists
            from .models import UserProfile
            if not hasattr(user, 'profile'):
                # Fallback for old admin users
                UserProfile.objects.create(user=user, role='ADMIN')

            refresh = RefreshToken.for_user(user)
            # Add custom claim to token
            refresh['role'] = user.profile.role

            return Response({
                'status': 'success',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'role': user.profile.role,
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_superuser': user.is_superuser,
                    'role': user.profile.role
                }
            }, status=status.HTTP_200_OK)
            
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserListView(APIView):
    permission_classes = [AllowAny] # Ideally restricted to Admin

    def get(self, request):
        User = get_user_model()
        users = User.objects.all().values('id', 'username', 'email', 'date_joined', 'is_active', 'last_login')
        return Response(list(users), status=status.HTTP_200_OK)

from rest_framework import viewsets
from .serializers import AdminUserSerializer

class AdminUserViewSet(viewsets.ModelViewSet):
    """
    CRUD for Admin Users.
    Only allows management of staff/superusers.
    """
    permission_classes = [AllowAny] # Security: In prod, restrict to SuperUser
    serializer_class = AdminUserSerializer
    
    def get_queryset(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        # Show all users who have a profile (System roles) but exclude normal Citizens
        # If a user has no profile (legacy root), include them too if they are staff
        return User.objects.filter(profile__isnull=False).exclude(profile__role='CITIZEN') | User.objects.filter(profile__isnull=True, is_staff=True)

    def perform_create(self, serializer):
        user = serializer.save()
        try:
            import requests
            # Actor is the current logged in admin (or SYSTEM if anonymous for now)
            actor = self.request.user.username if self.request.user.is_authenticated else 'SYSTEM'
            
            # Get role from the created profile if possible
            role_assigned = "UNKNOWN"
            if hasattr(user, 'profile'):
                role_assigned = user.profile.get_role_display()
            
            requests.post('http://127.0.0.1:8003/api/v1/audit/logs/', json={
                'action': 'CREATE_USER',
                'user_id': actor,
                'username': actor,
                'actor_type': 'ADMIN',
                'severity': 'WARNING',
                'details': f"Created new user '{user.username}' ({user.email}) with role '{role_assigned}'",
                'status': 'SUCCESS'
            }, timeout=1)
        except Exception as e:
            print(f"Audit Log Failed: {e}")

    def perform_update(self, serializer):
        user = serializer.save()
        try:
            import requests
            actor = self.request.user.username if self.request.user.is_authenticated else 'SYSTEM'
            
            requests.post('http://127.0.0.1:8003/api/v1/audit/logs/', json={
                'action': 'UPDATE_PROFILE',
                'user_id': actor,
                'username': actor,
                'actor_type': 'ADMIN',
                'severity': 'INFO',
                'details': f"Updated admin profile: {user.username}",
                'status': 'SUCCESS'
            }, timeout=1)
        except Exception as e:
            print(f"Audit Log Failed: {e}")

    def perform_destroy(self, instance):
        username = instance.username
        instance.delete()
        
        try:
            import requests
            requests.post('http://127.0.0.1:8003/api/v1/audit/logs/', json={
                'action': 'DELETE_ADMIN',
                'user_id': self.request.user.username if self.request.user.is_authenticated else 'SYSTEM',
                'username': self.request.user.username if self.request.user.is_authenticated else 'SYSTEM',
                'actor_type': 'ADMIN',
                'severity': 'CRITICAL',
                'details': f"Deleted admin user: {username}",
                'status': 'SUCCESS'
            }, timeout=1)
        except Exception as e:
            print(f"Audit Log Failed: {e}")
