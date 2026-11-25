
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid

from accounts.models import Retailer
from branches.models import Branch

from .constants import RETURN_STATUS


class SalesReturn(models.Model):

    retailer = models.ForeignKey(Retailer,on_delete=models.CASCADE,related_name="sales_returns")
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True,blank=True,related_name="sales_returns")
    return_no = models.CharField(max_length=50,unique=True,blank=True)
    sales = models.ForeignKey("Sales",on_delete=models.PROTECT,related_name="sales_returns")
    total_amount = models.DecimalField(max_digits=12,decimal_places=2,default=0,validators=[MinValueValidator(0)])
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20,choices=RETURN_STATUS,default="DRAFT")
    remarks = models.TextField( null=True,blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-id"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["sales"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["retailer", "branch"]),
            models.Index(fields=["retailer", "status"]),
            models.Index(fields=["branch", "status"]),
            models.Index(fields=["sales", "status"]),
            models.Index(fields=["created_at", "status"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(total_amount__gte=0),
                name="sales_return_total_amount_non_negative"
            ),
            models.CheckConstraint(
                condition=Q(refund_amount__gte=0),
                name="sales_return_refund_amount_non_negative"
            ),
            models.CheckConstraint(
                condition=Q(refund_amount__lte=models.F("total_amount")),
                name="sales_return_refund_not_exceed_total"
            ),
        ]

    def clean(self):

        super().clean()

        errors = {}

        if self.branch_id and self.retailer_id:
            if self.branch.retailer_id != self.retailer_id:
                errors["branch"] = (
                    "Selected branch does not belong to this retailer."
                )

        if self.sales_id and self.retailer_id:

            if self.sales.retailer_id != self.retailer_id:
                errors["sales"] = (
                    "Selected sale does not belong to this retailer."
                )

            if self.sales.branch_id != self.branch_id:
                errors["branch"] = (
                    "Sales return branch must match the original sale branch."
                )

        if self.total_amount is not None and self.total_amount < 0:
            errors["total_amount"] = (
                "Total amount cannot be negative."
            )

        if self.refund_amount is not None and self.refund_amount < 0:
            errors["refund_amount"] = (
                "Refund amount cannot be negative."
            )

        if (
            self.total_amount is not None
            and self.refund_amount is not None
            and self.refund_amount > self.total_amount
        ):
            errors["refund_amount"] = (
                "Refund amount cannot exceed total amount."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):

        generate_return_no = not self.return_no
        is_new = self._state.adding

        if generate_return_no:

            year = timezone.localdate().year

            if is_new:
                self.return_no = f"TEMP-{uuid.uuid4().hex}"
            else:
                self.return_no = (
                    f"SR-{year}-{self.pk:06d}"
                )

                if kwargs.get("update_fields") is not None:
                    kwargs["update_fields"] = (
                        set(kwargs["update_fields"]) | {"return_no"}
                    )

        self.full_clean()

        super().save(*args, **kwargs)

        if is_new and generate_return_no:

            year = timezone.localdate().year

            self.return_no = (
                f"SR-{year}-{self.pk:06d}"
            )

            super().save(update_fields=["return_no"])

    def __str__(self):

        return self.return_no
