from django.db import models
from django.db.models import Max
from datetime import datetime
from django.db import transaction
from .constants import TRANSACTION_TYPE, STOCK_TRANSACTION_STATUS
from django.conf import settings
from accounts.models import Retailer
from branches.models import Branch

class StockTransaction(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="stock_transactions")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="stock_transactions")
    transaction_no = models.CharField(max_length=50, unique=True, blank=True)
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPE)
    supplier = models.ForeignKey("masters.Supplier", on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey("masters.Customer",on_delete=models.SET_NULL,null=True,blank=True)
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
            models.Index(fields=["transaction_no"]),
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

    # =========================
    # AUTO TRANSACTION NUMBER
    # =========================

    def save(self, *args, **kwargs):

        if self.total_amount < 0:
            raise ValueError(
                "Total amount cannot be negative"
            )

        if not self.transaction_type:
            raise ValueError(
                "Transaction type is required"
            )

        if not self.transaction_no:

            year = datetime.now().year

            with transaction.atomic():

                last_transaction = (
                    StockTransaction.objects
                    .select_for_update()
                    .filter(
                        transaction_no__startswith=f"ST-{year}"
                    )
                    .order_by("-id")
                    .first()
                )

                next_number = 1

                if last_transaction:

                    try:
                        next_number = int(
                            last_transaction.transaction_no.split("-")[-1]
                        ) + 1

                    except Exception:
                        next_number = last_transaction.id + 1

                self.transaction_no = (
                    f"ST-{year}-{next_number:04d}"
                )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.transaction_no