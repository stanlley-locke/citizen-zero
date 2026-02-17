from django.db import models

class DigitalID(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('SUSPENDED', 'Suspended'),
        ('REVOKED', 'Revoked'),
    )

    TYPE_CHOICES = (
        ('NATIONAL_ID', 'National ID'),
        ('PASSPORT', 'Passport'),
        ('DRIVING_LICENSE', 'Driving License'),
    )

    national_id = models.CharField(max_length=20, unique=True, null=True)
    citizen_id = models.CharField(max_length=50) # Link to Auth Service User
    document_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='NATIONAL_ID')
    issuance_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    
    # Cryptographic fields
    public_key = models.TextField()
    doc_type = models.CharField(max_length=50, default='org.iso.18013.5.1.mDL')

    def __str__(self):
        return f"ID-{self.citizen_id}"

class IssuanceRequest(models.Model):
    citizen_id = models.CharField(max_length=20)
    doc_type = models.CharField(max_length=50) # DRIVING_LICENSE, PASSPORT, etc.
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='PENDING') # PENDING, APPROVED, REJECTED
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"REQ-{self.citizen_id}-{self.doc_type}"
