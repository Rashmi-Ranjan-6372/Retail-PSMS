from decimal import Decimal

from django.db import models
from django.db.models import Q, F
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from accounts.models import Retailer
from branches.models import Branch

from .constants import ADJUSTMENT_TYPE

class StockAdjustment(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="stock_adjustments")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="stock_adjustments")
    product = models.ForeignKey("masters.Product", on_delete=models.PROTECT)
    batch = models.ForeignKey("inventory.StockBatch", on_delete=models.PROTECT)
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

        constraints = [
            models.CheckConstraint(
                condition=Q(adjustment_qty__gt=0),
                name="stock_adjustment_qty_positive"
            ),
            models.CheckConstraint(
                condition=Q(unit_price__gte=0),
                name="stock_adjustment_unit_price_non_negative"
            ),
            models.CheckConstraint(
                condition=Q(total_value__gte=0),
                name="stock_adjustment_total_value_non_negative"
            ),
        ]

    def clean(self):

        super().clean()

        errors = {}

        if self.adjustment_type:
            valid_types = [
                choice[0] for choice in ADJUSTMENT_TYPE
            ]

            if self.adjustment_type not in valid_types:
                errors["adjustment_type"] = (
                    "Invalid adjustment type."
                )

        if self.adjustment_qty is not None and self.adjustment_qty <= 0:
            errors["adjustment_qty"] = (
                "Adjustment quantity must be greater than 0."
            )

        if self.unit_price is not None and self.unit_price < 0:
            errors["unit_price"] = (
                "Unit price cannot be negative."
            )

        if self.retailer_id and self.branch_id:

            if self.branch.retailer_id != self.retailer_id:
                errors["branch"] = (
                    "Selected branch does not belong to this retailer."
                )

        if self.retailer_id and self.product_id:

            if self.product.retailer_id != self.retailer_id:
                errors["product"] = (
                    "Selected product does not belong to this retailer."
                )

        if self.retailer_id and self.batch_id:

            if self.batch.retailer_id != self.retailer_id:
                errors["batch"] = (
                    "Selected batch does not belong to this retailer."
                )

        if self.product_id and self.batch_id:

            if self.batch.product_id != self.product_id:
                errors["batch"] = (
                    "Selected batch does not belong to this product."
                )

        if self.branch_id and self.batch_id:

            if self.batch.branch_id != self.branch_id:
                errors["batch"] = (
                    "Selected batch does not belong to this branch."
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):

        if self.adjustment_qty is None or self.adjustment_qty <= 0:
            raise ValidationError(
                "Adjustment quantity must be greater than 0."
            )

        if self.unit_price is None or self.unit_price < 0:
            raise ValidationError(
                "Unit price cannot be negative."
            )

        self.total_value = (
            Decimal(self.adjustment_qty) * self.unit_price
        )

        update_fields = kwargs.get("update_fields")

        if update_fields is not None:
            kwargs["update_fields"] = (
                set(update_fields) | {"total_value"}
            )

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.product.name} "
            f"({self.adjustment_type})"
        )
