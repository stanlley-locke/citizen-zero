from django.db import models
from apps.citizens.models import Citizen

class FaceBiometric(models.Model):
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='face_biometrics')
    image_path = models.CharField(max_length=255) # Path relative to media root
    encoding = models.BinaryField(blank=True, null=True) # NumPy array bytes or similar
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Face: {self.citizen.national_id}"

class FingerprintBiometric(models.Model):
    FINGER_CHOICES = [
        ('L_THUMB', 'Left Thumb'),
        ('L_INDEX', 'Left Index'),
        ('R_THUMB', 'Right Thumb'),
        ('R_INDEX', 'Right Index'),
        # ... others
    ]
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='fingerprints')
    finger_type = models.CharField(max_length=20, choices=FINGER_CHOICES)
    template_data = models.BinaryField() # ISO template bytes
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.finger_type}: {self.citizen.national_id}"
