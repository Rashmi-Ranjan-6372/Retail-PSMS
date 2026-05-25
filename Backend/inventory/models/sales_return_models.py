from django.db import models
from django.db.models import Max
from datetime import datetime
from django.db import transaction
from .constants import STATUS
from django.conf import settings
from accounts.models import Retailer
from branches.models import Branch

class SalesReturn(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="sales_returns")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales_returns")
    return_no = models.CharField(max_length=50, unique=True, blank=True)
    sales = models.ForeignKey("Sales", on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS, default="COMPLETED")
    remarks = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

        indexes = [
            models.Index(fields=["return_no"]),
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

    def save(self, *args, **kwargs):

        if not self.return_no:

            year = datetime.now().year

            with transaction.atomic():

                last_id = (
                    SalesReturn.objects.filter(
                        return_no__startswith=f"SR-{year}"
                    ).aggregate(
                        Max("id")
                    )["id__max"] or 0
                )

                self.return_no = (
                    f"SR-{year}-{last_id + 1:04d}"
                )

        if self.total_amount < 0:
            raise ValueError(
                "Total amount cannot be negative"
            )

        if self.refund_amount < 0:
            raise ValueError(
                "Refund amount cannot be negative"
            )

        if self.refund_amount > self.total_amount:
            raise ValueError(
                "Refund amount cannot exceed total amount"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.return_no