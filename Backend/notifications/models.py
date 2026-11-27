
from django.conf import settings
from django.db import models


class Notification(models.Model):

    NOTIFICATION_SCOPES = (
        ("platform", "Platform"),
        ("retailer", "Retailer"),
    )

    NOTIFICATION_TYPES = (
        ("new_retailer", "New Retailer Registered"),
        ("subscription_created", "Subscription Created"),
        ("subscription_expiring", "Subscription Expiring"),
        ("subscription_expired", "Subscription Expired"),
        ("payment_received", "Payment Received"),
        ("payment_failed", "Payment Failed"),
        ("low_stock", "Low Stock"),
        ("expiry_soon", "Expiry Soon"),
        ("expired_product", "Expired Product"),
        ("sale_completed", "Sale Completed"),
        ("purchase_received", "Purchase Received"),
        ("stock_transfer_received", "Stock Transfer Received"),
        ("staff_added", "Staff Added"),
        ("backup_completed", "Backup Completed"),
        ("backup_failed", "Backup Failed"),
        ("system_alert", "System Alert"),
        ("general", "General"),
    )

    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("normal", "Normal"),
        ("high", "High"),
        ("critical", "Critical"),
    )

    scope = models.CharField(max_length=20,choices=NOTIFICATION_SCOPES,default="retailer",)
    retailer = models.ForeignKey("accounts.Retailer",on_delete=models.CASCADE,related_name="notifications",null=True,blank=True,)
    branch = models.ForeignKey("branches.Branch",on_delete=models.CASCADE,related_name="notifications",null=True,blank=True,)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="notifications",)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50,choices=NOTIFICATION_TYPES,default="general",)
    priority = models.CharField(max_length=20,choices=PRIORITY_CHOICES,default="normal",)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True,blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["recipient", "is_read", "-created_at"],
                name="notif_rec_read_created_idx",
            ),
            models.Index(
                fields=["scope", "created_at"],
                name="notif_scope_created_idx",
            ),
            models.Index(
                fields=["retailer", "created_at"],
                name="notif_retailer_created_idx",
            ),
            models.Index(
                fields=["branch", "created_at"],
                name="notif_branch_created_idx",
            ),
        ]

    def __str__(self):
        return f"{self.title} - {self.recipient}"

    def mark_as_read(self):
        from django.utils import timezone

        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=["is_read", "read_at", "updated_at"])
