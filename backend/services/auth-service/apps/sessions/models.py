from django.db import models

class UserSession(models.Model):
    user_id = models.CharField(max_length=50)
    session_key = models.CharField(max_length=100)
    device_info = models.TextField()
    last_active = models.DateTimeField(auto_now=True)
