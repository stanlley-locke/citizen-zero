import os
import django
import sys
import random
from datetime import timedelta
from django.utils import timezone

# Setup Django Environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audit_service.settings')
django.setup()

from apps.audit_trail.models import AuditLog

def seed_logs():
    print("Seeding Audit Logs...")
    
    actions = [
        ('LOGIN', 'User Login via Mobile App'),
        ('VERIFY_ID', 'ID Verification by Third Party'),
        ('ISSUE_ID', 'Digital ID Issuance (Maisha Namba)'),
        ('UPDATE_PROFILE', 'Biometric Update Request'),
        ('LOGOUT', 'User Logout'),
    ]
    
    user_id = "12345678" # Demo User
    
    # Clear old logs
    AuditLog.objects.all().delete()
    
    # Create 10 logs
    for i in range(10):
        action, details = random.choice(actions)
        status = 'SUCCESS'
        
        # Random time in last 2 days
        time_offset = random.randint(0, 48 * 60)
        log_time = timezone.now() - timedelta(minutes=time_offset)
        
        log = AuditLog.objects.create(
            action=action,
            user_id=user_id,
            details=details,
            ip_address=f"192.168.1.{random.randint(2, 255)}",
            status=status
        )
        log.timestamp = log_time # Hack to override auto_now_add
        log.save()
        
    print(f"Successfully seeded {AuditLog.objects.count()} logs for user {user_id}")

if __name__ == '__main__':
    seed_logs()
