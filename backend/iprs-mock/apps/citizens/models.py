from django.db import models

class Citizen(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    national_id = models.CharField(max_length=20, unique=True, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    place_of_birth = models.CharField(max_length=100)
    county_of_birth = models.CharField(max_length=100) # e.g. "047 - Nairobi"
    
    # Contact info (simplified for mock)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.national_id})"
