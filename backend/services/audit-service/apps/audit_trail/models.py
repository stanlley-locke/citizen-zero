from django.db import models

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('LOGIN', 'User Login'),
        ('LOGOUT', 'User Logout'),
        ('ISSUE_ID', 'ID Issuance'),
        ('VERIFY_ID', 'ID Verification'),
        ('UPDATE_PROFILE', 'Profile Update'),
        ('ADMIN_LOGIN', 'Admin Login'),
        ('CREATE_ADMIN', 'Create Admin'),
        ('DELETE_ADMIN', 'Delete Admin'),
        ('IMPORT_DOCS', 'Import Documents'),
    ]

    SEVERITY_CHOICES = [
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('CRITICAL', 'Critical'),
    ]

    ACTOR_TYPE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('CITIZEN', 'Citizen'),
        ('SYSTEM', 'System')
    ]

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    user_id = models.CharField(max_length=100) # National ID or UUID
    username = models.CharField(max_length=150, null=True, blank=True) # Human readable name
    actor_type = models.CharField(max_length=20, choices=ACTOR_TYPE_CHOICES, default='SYSTEM')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    details = models.TextField(blank=True, null=True) # JSON or text details
    status = models.CharField(max_length=20, default='SUCCESS')
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='INFO')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action} - {self.user_id} - {self.timestamp}"
