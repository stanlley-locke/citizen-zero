from django.db import models
from apps.citizens.models import Citizen

class CitizenPhoto(models.Model):
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo: {self.citizen.national_id}"
