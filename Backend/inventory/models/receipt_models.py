from django.db import models
from django.db.models import Max
from datetime import datetime
from django.db import transaction
from .constants import RECEIPT_STATUS
from django.conf import settings

class Receipt(models.Model):
    receipt_no = models.CharField(max_length=50, unique=True, blank=True)

    customer = models.ForeignKey("masters.Customer", on_delete=models.CASCADE)
    branch = models.ForeignKey("branches.Branch", on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    payment_method = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=RECEIPT_STATUS, default="RECEIVED")

    reference_no = models.CharField(max_length=50, null=True, blank=True)

    remarks = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.receipt_no:
            year = datetime.now().year

            with transaction.atomic():
                last_id = Receipt.objects.filter(
                    receipt_no__startswith=f"RCPT-{year}"
                ).aggregate(Max("id"))["id__max"] or 0

                self.receipt_no = f"RCPT-{year}-{last_id + 1:04d}"

        self.due_amount = self.amount - self.paid_amount

        super().save(*args, **kwargs)

    def __str__(self):
        return self.receipt_no