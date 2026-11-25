
from decimal import Decimal

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from accounts.models import Retailer
from branches.models import Branch

from .constants import ADJUSTMENT_TYPE

class StockTransactionItem(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="stock_transaction_items")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="stock_transaction_items")
    transaction = models.ForeignKey("StockTransaction", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("masters.Product", on_delete=models.PROTECT)
    batch = models.ForeignKey("inventory.StockBatch", on_delete=models.PROTECT)
    movement_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPE)
    qty = models.PositiveIntegerField()
    free_qty = models.PositiveIntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    available_after = models.IntegerField(default=0)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-id"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["transaction"]),
            models.Index(fields=["product"]),
            models.Index(fields=["batch"]),
            models.Index(fields=["movement_type"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["retailer", "branch"]),
            models.Index(fields=["retailer", "product"]),
            models.Index(fields=["branch", "product"]),
            models.Index(fields=["product", "batch"]),
            models.Index(fields=["product", "movement_type"]),
            models.Index(fields=["batch", "movement_type"]),
            models.Index(fields=["transaction", "movement_type"]),
            models.Index(fields=["created_at", "movement_type"]),
            models.Index(fields=["expiry_date"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(qty__gt=0),
                name="stock_transaction_item_qty_positive"
            ),
            models.CheckConstraint(
                condition=Q(free_qty__gte=0),
                name="stock_transaction_item_free_qty_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(purchase_price__gte=0),
                name="stock_transaction_item_purchase_price_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(sale_price__gte=0),
                name="stock_transaction_item_sale_price_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(total_amount__gte=0),
                name="stock_transaction_item_total_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(available_after__gte=0),
                name="stock_transaction_item_available_after_nonnegative"
            ),
        ]

    def clean(self):

        super().clean()

        errors = {}

        valid_types = [
            choice[0] for choice in ADJUSTMENT_TYPE
        ]

        if (
            self.movement_type
            and self.movement_type not in valid_types
        ):
            errors["movement_type"] = (
                "Invalid stock movement type."
            )

        if self.transaction_id and self.retailer_id:

            if self.transaction.retailer_id != self.retailer_id:
                errors["transaction"] = (
                    "Transaction does not belong to this retailer."
                )

            if self.transaction.branch_id != self.branch_id:
                errors["branch"] = (
                    "Transaction branch must match the item branch."
                )

        if self.branch_id and self.retailer_id:

            if self.branch.retailer_id != self.retailer_id:
                errors["branch"] = (
                    "Branch does not belong to this retailer."
                )

        if self.product_id and self.retailer_id:

            if self.product.retailer_id != self.retailer_id:
                errors["product"] = (
                    "Product does not belong to this retailer."
                )

        if self.batch_id and self.retailer_id:

            if self.batch.retailer_id != self.retailer_id:
                errors["batch"] = (
                    "Batch does not belong to this retailer."
                )

        if self.product_id and self.batch_id:

            if self.batch.product_id != self.product_id:
                errors["batch"] = (
                    "Batch does not belong to this product."
                )

        if self.branch_id and self.batch_id:

            if self.batch.branch_id != self.branch_id:
                errors["batch"] = (
                    "Batch does not belong to this branch."
                )

        if self.expiry_date and self.batch_id:

            if self.batch.expiry_date != self.expiry_date:
                errors["expiry_date"] = (
                    "Expiry date must match the selected batch."
                )

        if self.qty is not None and self.qty <= 0:
            errors["qty"] = (
                "Quantity must be greater than 0."
            )

        if self.free_qty is not None and self.free_qty < 0:
            errors["free_qty"] = (
                "Free quantity cannot be negative."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):

        if self.qty is None or self.qty <= 0:
            raise ValidationError(
                {"qty": "Quantity must be greater than 0."}
            )

        if self.free_qty is None or self.free_qty < 0:
            raise ValidationError(
                {"free_qty": "Free quantity cannot be negative."}
            )

        if self.purchase_price is None or self.purchase_price < 0:
            raise ValidationError(
                {"purchase_price": "Purchase price cannot be negative."}
            )

        if self.sale_price is None or self.sale_price < 0:
            raise ValidationError(
                {"sale_price": "Sale price cannot be negative."}
            )

        if self.available_after is None or self.available_after < 0:
            raise ValidationError(
                {"available_after": "Available stock cannot be negative."}
            )

        self.total_amount = (
            Decimal(self.qty) * self.purchase_price
        )

        update_fields = kwargs.get("update_fields")

        if update_fields is not None:
            kwargs["update_fields"] = (
                set(update_fields) | {"total_amount"}
            )

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.product.name} "
            f"({self.movement_type})"
        )
