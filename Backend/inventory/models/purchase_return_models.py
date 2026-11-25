from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone

from accounts.models import Retailer
from branches.models import Branch

from .constants import RETURN_STATUS

class PurchaseReturn(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="purchase_returns")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="purchase_returns")
    return_no = models.CharField(max_length=50, unique=True, blank=True)
    supplier = models.ForeignKey("masters.Supplier", on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    adjusted_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=RETURN_STATUS, default="DRAFT")
    remarks = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["return_no"]),
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["supplier"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["retailer", "branch"]),
            models.Index(fields=["retailer", "supplier"]),
            models.Index(fields=["retailer", "status"]),
            models.Index(fields=["branch", "status"]),
            models.Index(fields=["supplier", "status"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(total_amount__gte=0),
                name="purchase_return_total_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(adjusted_amount__gte=0),
                name="purchase_return_adjusted_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(adjusted_amount__lte=models.F("total_amount")),
                name="purchase_return_adjusted_lte_total"
            ),
        ]

    def clean(self):
        super().clean()

        if self.total_amount is not None and self.total_amount < 0:
            raise ValidationError({
                "total_amount": "Total amount cannot be negative."
            })

        if self.adjusted_amount is not None and self.adjusted_amount < 0:
            raise ValidationError({
                "adjusted_amount": "Adjusted amount cannot be negative."
            })

        if (
            self.total_amount is not None
            and self.adjusted_amount is not None
            and self.adjusted_amount > self.total_amount
        ):
            raise ValidationError({
                "adjusted_amount": "Adjusted amount cannot exceed total amount."
            })

        if self.branch_id and self.branch.retailer_id != self.retailer_id:
            raise ValidationError({
                "branch": "Selected branch does not belong to this retailer."
            })

        if self.supplier_id and self.supplier.retailer_id != self.retailer_id:
            raise ValidationError({
                "supplier": "Selected supplier does not belong to this retailer."
            })

    def save(self, *args, **kwargs):

        if self.total_amount is None or self.total_amount < 0:
            raise ValidationError("Total amount cannot be negative.")

        if self.adjusted_amount is None or self.adjusted_amount < 0:
            raise ValidationError("Adjusted amount cannot be negative.")

        if self.adjusted_amount > self.total_amount:
            raise ValidationError(
                "Adjusted amount cannot exceed total amount."
            )

        if self.branch_id and self.branch.retailer_id != self.retailer_id:
            raise ValidationError(
                "Selected branch does not belong to this retailer."
            )

        if self.supplier_id and self.supplier.retailer_id != self.retailer_id:
            raise ValidationError(
                "Selected supplier does not belong to this retailer."
            )

        if not self.return_no:
            with transaction.atomic():
                if not self.pk:
                    super().save(*args, **kwargs)

                self.return_no = (
                    f"PR-{timezone.localdate().year}-{self.pk:06d}"
                )

                self.full_clean()

                super().save(
                    update_fields=["return_no", "updated_at"]
                )

            return

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.return_no
