from django.db import models
from django.db.models import Max
from datetime import datetime
from django.db import transaction
from .constants import STATUS
from django.conf import settings
from accounts.models import Retailer
from branches.models import Branch

class Sales(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="sales")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales")
    invoice_no = models.CharField(max_length=50, unique=True, blank=True)
    customer = models.ForeignKey("masters.Customer", on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, default="UNPAID")
    status = models.CharField(max_length=20, choices=STATUS, default="CONFIRMED")
    remarks = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
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

    # =========================
    # AUTO GENERATE INVOICE NO
    # =========================

    def save(self, *args, **kwargs):

        if not self.invoice_no:

            year = datetime.now().year

            with transaction.atomic():

                last_id = (
                    Sales.objects.filter(
                        invoice_no__startswith=f"INV-{year}"
                    ).aggregate(
                        Max("id")
                    )["id__max"] or 0
                )

                self.invoice_no = (
                    f"INV-{year}-{last_id + 1:04d}"
                )

        if self.total_amount < 0:
            raise ValueError(
                "Total amount cannot be negative"
            )

        if self.discount < 0:
            raise ValueError(
                "Discount cannot be negative"
            )

        if self.paid_amount < 0:
            raise ValueError(
                "Paid amount cannot be negative"
            )

        if self.discount > self.total_amount:
            raise ValueError(
                "Discount cannot exceed total amount"
            )

        self.net_amount = (
            (self.total_amount or 0) -
            (self.discount or 0)
        )

        if self.paid_amount > self.net_amount:
            raise ValueError(
                "Paid amount cannot exceed net amount"
            )

        self.due_amount = (
            self.net_amount -
            (self.paid_amount or 0)
        )

        if self.due_amount <= 0:

            self.payment_status = "PAID"

        elif self.paid_amount > 0:

            self.payment_status = "PARTIAL"

        else:

            self.payment_status = "UNPAID"

        super().save(*args, **kwargs)

        # =========================
        # CALCULATE NET AMOUNT
        # =========================

        self.net_amount = (
            (self.total_amount or 0) -
            (self.discount or 0)
        )

        self.due_amount = (
            self.net_amount -
            (self.paid_amount or 0)
        )

        # =========================
        # PAYMENT STATUS
        # =========================

        if self.due_amount <= 0:

            self.payment_status = "PAID"

        elif self.paid_amount > 0:

            self.payment_status = "PARTIAL"

        else:

            self.payment_status = "UNPAID"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_no