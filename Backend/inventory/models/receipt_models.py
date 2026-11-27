
from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone

from accounts.models import Retailer
from branches.models import Branch

from .constants import PAYMENT_METHOD, RECEIPT_STATUS

class Receipt(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.PROTECT, related_name="receipts")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="receipts")
    receipt_no = models.CharField(max_length=50, unique=True, blank=True)
    customer = models.ForeignKey("masters.Customer", on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20, choices=RECEIPT_STATUS, default="RECEIVED")
    reference_no = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["receipt_no"]),
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["customer"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["retailer", "branch"]),
            models.Index(fields=["retailer", "customer"]),
            models.Index(fields=["retailer", "status"]),
            models.Index(fields=["branch", "status"]),
            models.Index(fields=["customer", "status"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(amount__gt=0),
                name="receipt_amount_positive"
            ),
            models.CheckConstraint(
                condition=Q(paid_amount__gte=0),
                name="receipt_paid_amount_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(due_amount__gte=0),
                name="receipt_due_amount_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(paid_amount__lte=models.F("amount")),
                name="receipt_paid_not_exceed_amount"
            ),
            models.CheckConstraint(
                condition=Q(
                    due_amount=models.F("amount") - models.F("paid_amount")
                ),
                name="receipt_due_matches_amount"
            ),
        ]

    def clean(self):
        super().clean()

        if self.amount is not None and self.amount <= 0:
            raise ValidationError({
                "amount": "Receipt amount must be greater than zero."
            })

        if self.paid_amount is not None and self.paid_amount < 0:
            raise ValidationError({
                "paid_amount": "Paid amount cannot be negative."
            })

        if (
            self.amount is not None
            and self.paid_amount is not None
            and self.paid_amount > self.amount
        ):
            raise ValidationError({
                "paid_amount": "Paid amount cannot exceed receipt amount."
            })

        if self.branch_id and self.branch.retailer_id != self.retailer_id:
            raise ValidationError({
                "branch": "Selected branch does not belong to this retailer."
            })

        if self.customer_id and self.customer.retailer_id != self.retailer_id:
            raise ValidationError({
                "customer": "Selected customer does not belong to this retailer."
            })

    def save(self, *args, **kwargs):

        if self.amount is None or self.amount <= 0:
            raise ValidationError(
                "Receipt amount must be greater than zero."
            )

        if self.paid_amount is None or self.paid_amount < 0:
            raise ValidationError(
                "Paid amount cannot be negative."
            )

        if self.paid_amount > self.amount:
            raise ValidationError(
                "Paid amount cannot exceed receipt amount."
            )

        self.due_amount = self.amount - self.paid_amount

        if self.due_amount == 0:
            self.status = "RECEIVED"

        elif self.paid_amount > 0:
            self.status = "PARTIAL"

        else:
            self.status = "PENDING"

        if not self.receipt_no:
            with transaction.atomic():
                if not self.pk:
                    super().save(*args, **kwargs)

                self.receipt_no = (
                    f"RCPT-{timezone.localdate().year}-{self.pk:06d}"
                )

                self.full_clean()

                super().save(
                    update_fields=["receipt_no", "due_amount", "status", "updated_at"]
                )

            return

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.receipt_no
