from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        # Governance / Registry Roles (Admin Dash)
        ('DATA_COLLECTOR', 'Field Data Collector (NRB/CRS)'),
        ('INVESTIGATOR', 'Investigation Officer (DCI/EACC)'),
        
        # Business / Org Roles (Employer Portal)
        ('DATA_CONTROLLER', 'Data Controller (CEO/PS)'),
        ('DPO', 'Data Protection Officer'),
        ('ORG_ADMIN', 'System Administrator (Org)'),
        ('HR_MANAGER', 'Human Resource Manager'),
        ('INT_AUDITOR', 'Internal Auditor'),
        ('VERIFIER', 'Verifier / Enrollment Officer'),

        # Citizen
        ('CITIZEN', 'Citizen'),
        
        # Legacy/System
        ('SYSTEM_ADMIN', 'System Admin (Platform)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CITIZEN')
    organization = models.CharField(max_length=100, blank=True, null=True) 

    def __str__(self):
        return f"{self.user.username} - {self.role}"
