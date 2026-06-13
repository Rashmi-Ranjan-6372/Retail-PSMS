from django.db import models
from django.conf import settings
from accounts.models import Retailer


class BackupLog(models.Model):
    BACKUP_TYPE_CHOICES = (
        ("manual", "Manual"),
        ("automatic", "Automatic"),
    )

    BACKUP_SCOPE_CHOICES = (
        ("database", "Database"),
        ("media", "Media"),
        ("full", "Full"),
    )

    STATUS_CHOICES = (
        ("success", "Success"),
        ("failed", "Failed"),
        ("restored", "Restored"),
    )

    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, null=True, blank=True,related_name="backups")
    backup_type = models.CharField(max_length=20, choices=BACKUP_TYPE_CHOICES)
    backup_scope = models.CharField(max_length=20, choices=BACKUP_SCOPE_CHOICES, default="database")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default="success")
    file_name = models.CharField(max_length=255)
    file_path = models.TextField(null=True, blank=True)
    file_size = models.BigIntegerField(default=0, help_text="Size in bytes")
    checksum = models.CharField(max_length=255, null=True, blank=True)
    download_count = models.PositiveIntegerField(default=0)
    notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True, blank=True,related_name="created_backups")
    restored_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="restored_backups")
    created_at = models.DateTimeField(auto_now_add=True)
    restored_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.file_name} - {self.backup_type}"

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["backup_type"]),
            models.Index(fields=["backup_scope"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["retailer", "created_at"]),
        ]


class BackupSchedule(models.Model):
    FREQUENCY_CHOICES = (
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    )

    retailer = models.OneToOneField(Retailer, on_delete=models.CASCADE, related_name="backup_schedule")
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    backup_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.retailer.name} - "
            f"{self.frequency}"
        )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["frequency"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["backup_time"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["frequency", "is_active"]),
        ]