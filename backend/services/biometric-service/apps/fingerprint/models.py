from django.db import models

class Fingerprint(models.Model):
    citizen_id = models.CharField(max_length=50)
    finger_index = models.IntegerField(help_text="1-10 for standard ISO fingers")
    minutiae_template = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)
