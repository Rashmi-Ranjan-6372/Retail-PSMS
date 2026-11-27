from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q

from accounts.models import Retailer
from branches.models import Branch
from .constants import PAYMENT_METHOD, PAYMENT_STATUS


class Payment(models.Model):
    retailer = models.ForeignKey(
        Retailer, on_delete=models.CASCADE, related_name="payments"
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    payment_no = models.CharField(max_length=50, unique=True, blank=True)
    supplier = models.ForeignKey("masters.Supplier", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="UNPAID")
    reference_no = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -------------------------
    # AUTO GENERATE PAYMENT NO
    # -------------------------

    class Meta:

        ordering = ["-created_at"]

        indexes = [
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
                condition=Q(amount__gt=0),
                name="payment_amount_positive",
            ),
            models.CheckConstraint(
                condition=Q(paid_amount__gte=0),
                name="payment_paid_amount_nonnegative",
            ),
            models.CheckConstraint(
                condition=Q(due_amount__gte=0),
                name="payment_due_amount_nonnegative",
            ),
            models.CheckConstraint(
                condition=Q(paid_amount__lte=models.F("amount")),
                name="payment_paid_not_exceed_amount",
            ),
            models.CheckConstraint(
                condition=Q(due_amount=models.F("amount") - models.F("paid_amount")),
                name="payment_due_matches_amount",
            ),
        ]

    # =====================================================
    # MODEL VALIDATION
    # =====================================================

    def clean(self):

        super().clean()

        if self.amount is not None and self.amount <= 0:

            raise ValidationError(
                {"amount": "Payment amount must be greater than zero."}
            )

        if self.paid_amount is not None and self.paid_amount < 0:

            raise ValidationError({"paid_amount": "Paid amount cannot be negative."})

        if (
            self.amount is not None
            and self.paid_amount is not None
            and self.paid_amount > self.amount
        ):

            raise ValidationError(
                {"paid_amount": "Paid amount cannot exceed payment amount."}
            )

        if self.branch_id:

            if self.branch.retailer_id != self.retailer_id:

                raise ValidationError(
                    {"branch": "Selected branch does not belong to this retailer."}
                )

        if self.supplier_id:

            if self.supplier.retailer_id != self.retailer_id:

                raise ValidationError(
                    {"supplier": "Selected supplier does not belong to this retailer."}
                )

    # =====================================================
    # AUTO CALCULATE PAYMENT
    # =====================================================

    def calculate_payment(self):

        self.due_amount = self.amount - self.paid_amount

        if self.due_amount == 0:
            self.status = "PAID"

        elif self.paid_amount > 0:
            self.status = "PARTIAL"

        else:
            self.status = "UNPAID"

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, *args, **kwargs):

        if self.amount is None or self.amount <= 0:
            raise ValidationError("Payment amount must be greater than zero.")

        if self.paid_amount is None or self.paid_amount < 0:
            raise ValidationError("Paid amount cannot be negative.")

        if self.paid_amount > self.amount:
            raise ValidationError("Paid amount cannot exceed payment amount.")

        self.calculate_payment()

        update_fields = kwargs.get("update_fields")

        if update_fields is not None:

            update_fields = set(update_fields)

            update_fields.update(
                {
                    "due_amount",
                    "status",
                    "updated_at",
                }
            )

            if not self.payment_no:
                update_fields.add("payment_no")

            kwargs["update_fields"] = update_fields

        self.full_clean()

        if not self.payment_no:

            with transaction.atomic():

                super().save(*args, **kwargs)

                self.payment_no = f"PAY-{timezone.localdate().year}-{self.pk:06d}"

                super().save(
                    update_fields=[
                        "payment_no",
                        "updated_at",
                    ]
                )

            return

        super().save(*args, **kwargs)

    def __str__(self):

        return self.payment_no
