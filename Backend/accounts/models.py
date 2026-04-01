from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


# ================= USER MODEL ================= #
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='staff'
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    password_changed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_user = User.objects.filter(pk=self.pk).first()
            if old_user and old_user.password != self.password:
                self.password_changed_at = self.updated_at
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"

    class Meta:
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['role']),
        ]


# ================= LOGIN LOG ================= #
class LoginLog(models.Model):
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='success'
    )

    def __str__(self):
        return f"{self.user} - {self.login_time}"

    class Meta:
        ordering = ['-login_time']

# ================= USER SESSION ================= #
class UserSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    device_id = models.CharField(max_length=255)
    refresh_token = models.TextField()

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.device_id} - {self.is_active}"