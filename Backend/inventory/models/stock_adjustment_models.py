from django.db import models
from .constants import ADJUSTMENT_TYPE
from django.conf import settings
from accounts.models import Retailer
from branches.models import Branch

class StockAdjustment(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="stock_adjustments")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="stock_adjustments")
    product = models.ForeignKey("masters.Product", on_delete=models.CASCADE)
    batch = models.ForeignKey("inventory.StockBatch", on_delete=models.CASCADE)
    adjustment_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPE)
    adjustment_qty = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reason = models.CharField(max_length=255)
    remarks = models.TextField(null=True, blank=True)
    reference_no = models.CharField(max_length=50, null=True, blank=True)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-id"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["product"]),
            models.Index(fields=["batch"]),
            models.Index(fields=["adjustment_type"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["retailer", "branch"]),
            models.Index(fields=["retailer", "product"]),
            models.Index(fields=["branch", "product"]),
            models.Index(fields=["product", "batch"]),
            models.Index(fields=["retailer", "adjustment_type"]),
            models.Index(fields=["branch", "adjustment_type"]),
            models.Index(fields=["created_at", "adjustment_type"]),
        ]

    # =========================
    # AUTO CALCULATE VALUE
    # =========================

    def save(self, *args, **kwargs):

        if self.adjustment_qty <= 0:
            raise ValueError(
                "Adjustment quantity must be greater than 0"
            )

        if self.unit_price < 0:
            raise ValueError(
                "Unit price cannot be negative"
            )

        self.total_value = (
            (self.adjustment_qty or 0) *
            (self.unit_price or 0)
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.product.name} "
            f"({self.adjustment_type})"
        )