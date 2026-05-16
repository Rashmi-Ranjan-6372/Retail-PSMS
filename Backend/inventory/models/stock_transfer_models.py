from django.db import models
from datetime import datetime
from django.db.models import Max
from django.db import transaction
from .constants import TRANSFER_STATUS
from django.conf import settings
from accounts.models import Retailer
from branches.models import Branch

class StockTransfer(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="stock_transfers")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="stock_transfers")
    transfer_no = models.CharField(max_length=50, unique=True, blank=True)
    from_branch = models.ForeignKey("branches.Branch",on_delete=models.CASCADE,related_name="stock_out")
    to_branch = models.ForeignKey("branches.Branch",on_delete=models.CASCADE,related_name="stock_in")
    product = models.ForeignKey("masters.Product", on_delete=models.CASCADE)
    batch = models.ForeignKey("inventory.StockBatch", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=TRANSFER_STATUS, default="PENDING")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-id"]

        indexes = [
            models.Index(fields=["transfer_no"]),
            models.Index(fields=["retailer"]),
            models.Index(fields=["from_branch"]),
            models.Index(fields=["to_branch"]),
            models.Index(fields=["product"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    # =========================
    # AUTO TRANSFER NUMBER
    # =========================

    def save(self, *args, **kwargs):

        if not self.transfer_no:

            year = datetime.now().year

            with transaction.atomic():

                last_id = (
                    StockTransfer.objects.filter(
                        transfer_no__startswith=f"TR-{year}"
                    ).aggregate(Max("id"))["id__max"] or 0
                )

                self.transfer_no = (
                    f"TR-{year}-{last_id + 1:04d}"
                )

        self.total_cost = (
            (self.quantity or 0) *
            (self.unit_cost or 0)
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.transfer_no