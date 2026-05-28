from django.db import models
from django.conf import settings
from accounts.models import Retailer


class GeneralSetting(models.Model):
    retailer = models.OneToOneField(Retailer, on_delete=models.CASCADE, related_name="general_setting")
    currency = models.CharField(max_length=10, default="INR")
    timezone = models.CharField(max_length=100, default="Asia/Kolkata")
    low_stock_limit = models.PositiveIntegerField(default=10)
    enable_gst = models.BooleanField(default=True)
    enable_barcode = models.BooleanField(default=True)
    enable_expiry_alert = models.BooleanField(default=True)
    enable_loose_sale = models.BooleanField(default=True)
    enable_negative_stock = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-id"]

        indexes = [
            models.Index(fields=["retailer"]),
        ]

    def __str__(self):

        return (
            f"{self.retailer.name} Settings"
        )