
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import Q

from accounts.models import Retailer
from branches.models import Branch

from .constants import RETURN_CONDITION

class PurchaseReturnItem(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="purchase_return_items")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="purchase_return_items")
    purchase_return = models.ForeignKey("PurchaseReturn", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("masters.Product", on_delete=models.CASCADE)
    batch = models.ForeignKey("inventory.StockBatch", on_delete=models.CASCADE)
    qty = models.IntegerField()
    free_qty = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    return_condition = models.CharField(max_length=20, choices=RETURN_CONDITION, default="GOOD")
    remarks = models.TextField(null=True, blank=True)
    
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
            models.Index(fields=["return_condition"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["retailer", "branch"]),
            models.Index(fields=["retailer", "product"]),
            models.Index(fields=["branch", "product"]),
            models.Index(fields=["product", "batch"]),
            models.Index(fields=["retailer", "return_condition"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(qty__gte=1),
                name="purchase_return_item_qty_positive"
            ),
            models.CheckConstraint(
                condition=Q(free_qty__gte=0),
                name="purchase_return_item_free_qty_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(unit_price__gte=0),
                name="purchase_return_item_unit_price_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(amount__gte=0),
                name="purchase_return_item_amount_nonnegative"
            ),
        ]

    def clean(self):
        super().clean()

        if self.qty is not None and self.qty <= 0:
            raise ValidationError({
                "qty": "Return quantity must be greater than zero."
            })

        if self.free_qty is not None and self.free_qty < 0:
            raise ValidationError({
                "free_qty": "Free quantity cannot be negative."
            })

        if self.unit_price is not None and self.unit_price < 0:
            raise ValidationError({
                "unit_price": "Unit price cannot be negative."
            })

        if self.branch_id and self.branch.retailer_id != self.retailer_id:
            raise ValidationError({
                "branch": "Selected branch does not belong to this retailer."
            })

        if self.purchase_return_id:
            if self.purchase_return.retailer_id != self.retailer_id:
                raise ValidationError({
                    "purchase_return": "Purchase return does not belong to this retailer."
                })

            if self.purchase_return.branch_id != self.branch_id:
                raise ValidationError({
                    "branch": "Branch does not match the selected purchase return."
                })

        if self.product_id and self.product.retailer_id != self.retailer_id:
            raise ValidationError({
                "product": "Selected product does not belong to this retailer."
            })

        if self.batch_id:
            if self.batch.retailer_id != self.retailer_id:
                raise ValidationError({
                    "batch": "Selected batch does not belong to this retailer."
                })

            if self.batch.product_id != self.product_id:
                raise ValidationError({
                    "batch": "Selected batch does not belong to this product."
                })

            if self.batch.branch_id != self.branch_id:
                raise ValidationError({
                    "batch": "Selected batch does not belong to this branch."
                })

    def save(self, *args, **kwargs):
        if self.qty is None or self.qty <= 0:
            raise ValidationError("Return quantity must be greater than zero.")

        if self.free_qty is None or self.free_qty < 0:
            raise ValidationError("Free quantity cannot be negative.")

        if self.unit_price is None or self.unit_price < 0:
            raise ValidationError("Unit price cannot be negative.")

        self.amount = self.qty * self.unit_price

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} ({self.qty})"
