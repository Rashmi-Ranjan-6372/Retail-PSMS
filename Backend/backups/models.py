from django.db import models
from django.conf import settings
from accounts.models import Retailer


class BackupLog(models.Model):

    BACKUP_TYPE_CHOICES = (
        ("manual", "Manual"),
        ("automatic", "Automatic"),
    )

    STATUS_CHOICES = (
        ("success", "Success"),
        ("failed", "Failed"),
        ("restored", "Restored"),
    )

    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, null=True, blank=True, related_name="backups")
    backup_type = models.CharField(max_length=20, choices=BACKUP_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="success")
    file_name = models.CharField(max_length=255)
    file_path = models.TextField(null=True, blank=True)
    file_size = models.BigIntegerField(default=0, help_text="Size in bytes")
    notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_backups")
    created_at = models.DateTimeField(auto_now_add=True)
    restored_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return (
            f"{self.file_name} - "f"{self.backup_type}"
        )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["backup_type"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["retailer", "created_at"]),
        ]