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
    branch = models.ForeignKey("branches.Branch", on_delete=models.CASCADE)
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
        ]

    # =========================
    # AUTO TRANSACTION NUMBER
    # =========================

    def save(self, *args, **kwargs):

        if not self.transaction_no:

            year = datetime.now().year

            with transaction.atomic():

                last_id = (
                    StockTransaction.objects.filter(
                        transaction_no__startswith=f"ST-{year}"
                    ).aggregate(Max("id"))["id__max"] or 0
                )

                self.transaction_no = (
                    f"ST-{year}-{last_id + 1:04d}"
                )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.transaction_no