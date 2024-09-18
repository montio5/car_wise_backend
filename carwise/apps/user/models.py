from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class UserFCMToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fcm_tokens")
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.token}"


class PasswordResetRequest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="password_resets"
    )
    code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.code}"


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.token
