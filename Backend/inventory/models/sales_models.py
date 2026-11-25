from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import Q, F
from django.utils import timezone

from accounts.models import Retailer
from branches.models import Branch

from .constants import SALE_STATUS, PAYMENT_STATUS


class Sales(models.Model):

    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="sales")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales")
    invoice_no = models.CharField(max_length=50, unique=True, blank=True)
    customer = models.ForeignKey("masters.Customer",on_delete=models.SET_NULL,null=True,blank=True,related_name="sales",)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="UNPAID")
    status = models.CharField(max_length=20, choices=SALE_STATUS, default="DRAFT")
    remarks = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]

        indexes = [
            models.Index(fields=["invoice_no"]),
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["customer"]),
            models.Index(fields=["payment_status"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["retailer", "branch"]),
            models.Index(fields=["retailer", "customer"]),
            models.Index(fields=["retailer", "payment_status"]),
            models.Index(fields=["retailer", "status"]),
            models.Index(fields=["branch", "status"]),
            models.Index(fields=["customer", "payment_status"]),
            models.Index(fields=["created_at", "status"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(total_amount__gte=0), name="sales_total_amount_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(discount__gte=0), name="sales_discount_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(net_amount__gte=0), name="sales_net_amount_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(paid_amount__gte=0), name="sales_paid_amount_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(due_amount__gte=0), name="sales_due_amount_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(discount__lte=F("total_amount")),
                name="sales_discount_lte_total",
            ),
            models.CheckConstraint(
                condition=Q(net_amount=F("total_amount") - F("discount")),
                name="sales_net_matches_total_discount",
            ),
            models.CheckConstraint(
                condition=Q(paid_amount__lte=F("net_amount")), name="sales_paid_lte_net"
            ),
            models.CheckConstraint(
                condition=Q(due_amount=F("net_amount") - F("paid_amount")),
                name="sales_due_matches_net_paid",
            ),
        ]

    def clean(self):
        super().clean()

        if self.total_amount is not None and self.total_amount < 0:
            raise ValidationError({"total_amount": "Total amount cannot be negative."})

        if self.discount is not None and self.discount < 0:
            raise ValidationError({"discount": "Discount cannot be negative."})

        if self.paid_amount is not None and self.paid_amount < 0:
            raise ValidationError({"paid_amount": "Paid amount cannot be negative."})

        if (
            self.total_amount is not None
            and self.discount is not None
            and self.discount > self.total_amount
        ):
            raise ValidationError({"discount": "Discount cannot exceed total amount."})

        if (
            self.net_amount is not None
            and self.paid_amount is not None
            and self.paid_amount > self.net_amount
        ):
            raise ValidationError(
                {"paid_amount": "Paid amount cannot exceed net amount."}
            )

        if self.branch_id and self.branch.retailer_id != self.retailer_id:
            raise ValidationError(
                {"branch": "Selected branch does not belong to this retailer."}
            )

        if self.customer_id and self.customer.retailer_id != self.retailer_id:
            raise ValidationError(
                {"customer": "Selected customer does not belong to this retailer."}
            )

    def save(self, *args, **kwargs):

        if self.total_amount is None or self.total_amount < 0:
            raise ValidationError("Total amount cannot be negative.")

        if self.discount is None or self.discount < 0:
            raise ValidationError("Discount cannot be negative.")

        if self.paid_amount is None or self.paid_amount < 0:
            raise ValidationError("Paid amount cannot be negative.")

        if self.discount > self.total_amount:
            raise ValidationError("Discount cannot exceed total amount.")

        self.net_amount = self.total_amount - self.discount

        if self.paid_amount > self.net_amount:
            raise ValidationError("Paid amount cannot exceed net amount.")

        self.due_amount = self.net_amount - self.paid_amount

        if self.due_amount == 0:
            self.payment_status = "PAID"

        elif self.paid_amount > 0:
            self.payment_status = "PARTIAL"

        else:
            self.payment_status = "UNPAID"

        if not self.invoice_no:
            with transaction.atomic():

                if not self.pk:
                    super().save(*args, **kwargs)

                self.invoice_no = f"INV-{timezone.localdate().year}-{self.pk:06d}"

                self.full_clean()

                super().save(
                    update_fields=[
                        "invoice_no",
                        "net_amount",
                        "due_amount",
                        "payment_status",
                        "updated_at",
                    ]
                )

            return

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_no
