from django.db import models
from django.db.models import Max
from datetime import datetime
from django.db import transaction

from django.conf import settings
from .constants import PAYMENT_STATUS

class Payment(models.Model):
    payment_no = models.CharField(max_length=50, unique=True, blank=True)
    supplier = models.ForeignKey("masters.Supplier", on_delete=models.CASCADE)
    branch = models.ForeignKey("branches.Branch", on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    payment_method = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="PAID")

    reference_no = models.CharField(max_length=50, null=True, blank=True)

    remarks = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # -------------------------
    # AUTO GENERATE PAYMENT NO
    # -------------------------
    def save(self, *args, **kwargs):

        if not self.payment_no:
            year = datetime.now().year

            with transaction.atomic():
                last_payment = Payment.objects.filter(
                    payment_no__startswith=f"PAY-{year}"
                ).aggregate(Max("id"))["id__max"] or 0

                next_number = last_payment + 1
                self.payment_no = f"PAY-{year}-{next_number:04d}"

        self.due_amount = self.amount - self.paid_amount

        super().save(*args, **kwargs)

    def __str__(self):
        return self.payment_no