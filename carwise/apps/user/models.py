from django.db import models
from django.utils import timezone

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.token