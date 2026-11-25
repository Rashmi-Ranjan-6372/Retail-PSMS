from decimal import Decimal

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid

from accounts.models import Retailer
from branches.models import Branch

from .constants import TRANSACTION_TYPE, STOCK_TRANSACTION_STATUS
class StockTransaction(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="stock_transactions")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="stock_transactions")
    transaction_no = models.CharField(max_length=50, unique=True, blank=True)
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPE)
    supplier = models.ForeignKey("masters.Supplier", on_delete=models.PROTECT, null=True, blank=True)
    customer = models.ForeignKey("masters.Customer",on_delete=models.PROTECT,null=True,blank=True)
    reference_no = models.CharField(max_length=50, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STOCK_TRANSACTION_STATUS, default="POSTED")
    remarks = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-id"]

        indexes = [
            models.Index(fields=["transaction_type"]),
            models.Index(fields=["status"]),
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["retailer", "branch"]),
            models.Index(fields=["retailer", "transaction_type"]),
            models.Index(fields=["retailer", "status"]),
            models.Index(fields=["branch", "status"]),
            models.Index(fields=["transaction_type", "status"]),
            models.Index(fields=["supplier"]),
            models.Index(fields=["customer"]),
            models.Index(fields=["reference_no"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(total_amount__gte=0),
                name="stock_transaction_total_nonnegative"
            ),
        ]

    def clean(self):

        super().clean()

        errors = {}

        valid_transaction_types = [
            choice[0] for choice in TRANSACTION_TYPE
        ]

        valid_statuses = [
            choice[0] for choice in STOCK_TRANSACTION_STATUS
        ]

        if (
            self.transaction_type
            and self.transaction_type not in valid_transaction_types
        ):
            errors["transaction_type"] = (
                "Invalid transaction type."
            )

        if self.status and self.status not in valid_statuses:
            errors["status"] = (
                "Invalid stock transaction status."
            )

        if self.branch_id and self.retailer_id:

            if self.branch.retailer_id != self.retailer_id:
                errors["branch"] = (
                    "Selected branch does not belong to this retailer."
                )

        if self.supplier_id and self.retailer_id:

            if self.supplier.retailer_id != self.retailer_id:
                errors["supplier"] = (
                    "Selected supplier does not belong to this retailer."
                )

        if self.customer_id and self.retailer_id:

            if self.customer.retailer_id != self.retailer_id:
                errors["customer"] = (
                    "Selected customer does not belong to this retailer."
                )

        if self.total_amount is not None and self.total_amount < 0:
            errors["total_amount"] = (
                "Total amount cannot be negative."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):

        if not self.transaction_type:
            raise ValidationError(
                {"transaction_type": "Transaction type is required."}
            )

        if self.total_amount is None or self.total_amount < 0:
            raise ValidationError(
                {"total_amount": "Total amount cannot be negative."}
            )

        is_new = self._state.adding
        generate_transaction_no = not self.transaction_no

        if generate_transaction_no and is_new:
            self.transaction_no = f"TEMP-{uuid.uuid4().hex}"

        self.full_clean()

        super().save(*args, **kwargs)

        if is_new and generate_transaction_no:

            year = timezone.localdate().year

            self.transaction_no = (
                f"ST-{year}-{self.pk:06d}"
            )

            super().save(update_fields=["transaction_no"])

    def __str__(self):

        return self.transaction_no
