from django.db import models
from django.db.models import Max
from datetime import datetime
from django.db import transaction

from django.conf import settings
from .constants import PAYMENT_STATUS
from accounts.models import Retailer
from branches.models import Branch

class Payment(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="payments")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="payments")
    payment_no = models.CharField(max_length=50, unique=True, blank=True)
    supplier = models.ForeignKey("masters.Supplier", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="PAID")
    reference_no = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -------------------------
    # AUTO GENERATE PAYMENT NO
    # -------------------------

    class Meta:

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["payment_no"]),
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["supplier"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    # =========================
    # AUTO GENERATE PAYMENT NO
    # =========================

    def save(self, *args, **kwargs):

        if not self.payment_no:

            year = datetime.now().year

            with transaction.atomic():

                last_id = (
                    Payment.objects.filter(
                        payment_no__startswith=f"PAY-{year}"
                    ).aggregate(
                        max_id=Max("id")
                    )["max_id"] or 0
                )

                next_number = last_id + 1

                self.payment_no = (
                    f"PAY-{year}-{next_number:04d}"
                )

        # =========================
        # DUE CALCULATION
        # =========================

        self.due_amount = (
            self.amount - self.paid_amount
        )

        # =========================
        # PAYMENT STATUS
        # =========================

        if self.due_amount <= 0:
            self.status = "PAID"

        elif self.paid_amount > 0:
            self.status = "PARTIAL"

        else:
            self.status = "PENDING"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.payment_no