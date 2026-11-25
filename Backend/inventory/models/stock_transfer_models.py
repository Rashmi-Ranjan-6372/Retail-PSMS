
from decimal import Decimal
import uuid

from django.db import models
from django.db.models import F, Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone

from accounts.models import Retailer
from branches.models import Branch

from .constants import TRANSFER_STATUS
class StockTransfer(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="stock_transfers")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="stock_transfers")
    transfer_no = models.CharField(max_length=50, unique=True, blank=True)
    from_branch = models.ForeignKey("branches.Branch",on_delete=models.PROTECT,related_name="stock_out")
    to_branch = models.ForeignKey("branches.Branch",on_delete=models.PROTECT,related_name="stock_in")
    product = models.ForeignKey("masters.Product", on_delete=models.PROTECT)
    batch = models.ForeignKey("inventory.StockBatch", on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=TRANSFER_STATUS, default="PENDING")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-id"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["from_branch"]),
            models.Index(fields=["to_branch"]),
            models.Index(fields=["product"]),
            models.Index(fields=["batch"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["retailer", "status"]),
            models.Index(fields=["from_branch", "status"]),
            models.Index(fields=["to_branch", "status"]),
            models.Index(fields=["from_branch", "to_branch"]),
            models.Index(fields=["product", "batch"]),
            models.Index(fields=["retailer", "product"]),
            models.Index(fields=["created_at", "status"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gt=0),
                name="stock_transfer_quantity_positive"
            ),
            models.CheckConstraint(
                condition=Q(unit_cost__gte=0),
                name="stock_transfer_unit_cost_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(total_cost__gte=0),
                name="stock_transfer_total_cost_nonnegative"
            ),
            models.CheckConstraint(
                condition=~Q(from_branch=F("to_branch")),
                name="stock_transfer_different_branches"
            ),
        ]

    def clean(self):

        super().clean()

        errors = {}

        valid_statuses = [
            choice[0] for choice in TRANSFER_STATUS
        ]

        if self.status and self.status not in valid_statuses:
            errors["status"] = "Invalid transfer status."

        if (
            self.from_branch_id
            and self.to_branch_id
            and self.from_branch_id == self.to_branch_id
        ):
            errors["to_branch"] = (
                "Source and destination branches cannot be the same."
            )

        if self.retailer_id:

            if self.from_branch_id:
                if self.from_branch.retailer_id != self.retailer_id:
                    errors["from_branch"] = (
                        "Source branch does not belong to this retailer."
                    )

            if self.to_branch_id:
                if self.to_branch.retailer_id != self.retailer_id:
                    errors["to_branch"] = (
                        "Destination branch does not belong to this retailer."
                    )

            if self.product_id:
                if self.product.retailer_id != self.retailer_id:
                    errors["product"] = (
                        "Product does not belong to this retailer."
                    )

            if self.batch_id:
                if self.batch.retailer_id != self.retailer_id:
                    errors["batch"] = (
                        "Batch does not belong to this retailer."
                    )

        if self.product_id and self.batch_id:
            if self.batch.product_id != self.product_id:
                errors["batch"] = (
                    "Selected batch does not belong to this product."
                )

        if self.from_branch_id and self.batch_id:
            if self.batch.branch_id != self.from_branch_id:
                errors["batch"] = (
                    "Selected batch does not belong to the source branch."
                )

        if self.quantity is not None and self.quantity <= 0:
            errors["quantity"] = (
                "Transfer quantity must be greater than 0."
            )

        if self.unit_cost is not None and self.unit_cost < 0:
            errors["unit_cost"] = (
                "Unit cost cannot be negative."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):

        if self.quantity is None or self.quantity <= 0:
            raise ValidationError(
                {"quantity": "Quantity must be greater than 0."}
            )

        if self.unit_cost is None or self.unit_cost < 0:
            raise ValidationError(
                {"unit_cost": "Unit cost cannot be negative."}
            )

        is_new = self._state.adding
        generate_transfer_no = not self.transfer_no

        self.total_cost = (
            Decimal(self.quantity) * self.unit_cost
        )

        if generate_transfer_no and is_new:
            self.transfer_no = f"TEMP-{uuid.uuid4().hex}"

        update_fields = kwargs.get("update_fields")

        if update_fields is not None:
            kwargs["update_fields"] = (
                set(update_fields) | {"total_cost"}
            )

        self.full_clean()

        super().save(*args, **kwargs)

        if is_new and generate_transfer_no:

            year = timezone.localdate().year

            self.transfer_no = (
                f"TR-{year}-{self.pk:06d}"
            )

            super().save(update_fields=["transfer_no"])

    def __str__(self):

        return self.transfer_no
