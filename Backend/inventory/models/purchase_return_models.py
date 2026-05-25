from django.db import models
from django.db.models import Max
from datetime import datetime
from django.db import transaction
from .constants import STATUS
from django.conf import settings
from accounts.models import Retailer
from branches.models import Branch

class PurchaseReturn(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="purchase_returns")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="purchase_returns")
    return_no = models.CharField(max_length=50, unique=True, blank=True)
    supplier = models.ForeignKey("masters.Supplier", on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    adjusted_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS, default="DRAFT")
    remarks = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["return_no"]),
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

    # =========================
    # AUTO GENERATE RETURN NO
    # =========================

    def save(self, *args, **kwargs):

        if not self.return_no:

            year = datetime.now().year

            with transaction.atomic():

                last_id = (
                    PurchaseReturn.objects.filter(
                        return_no__startswith=f"PR-{year}"
                    ).aggregate(
                        max_id=Max("id")
                    )["max_id"] or 0
                )

                next_number = last_id + 1

                self.return_no = (
                    f"PR-{year}-{next_number:04d}"
                )

        if self.adjusted_amount > self.total_amount:
            raise ValueError(
                "Adjusted amount cannot exceed total amount"
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.return_no