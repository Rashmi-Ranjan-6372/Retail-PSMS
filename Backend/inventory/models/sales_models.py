from django.db import models
from django.db.models import Max
from datetime import datetime
from django.db import transaction
from .constants import STATUS
from django.conf import settings

class Sales(models.Model):
    invoice_no = models.CharField(max_length=50, unique=True, blank=True)
    customer = models.ForeignKey("masters.Customer", on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey("branches.Branch", on_delete=models.CASCADE)

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

    def save(self, *args, **kwargs):

        if not self.invoice_no:
            year = datetime.now().year

            with transaction.atomic():
                last_id = Sales.objects.filter(
                    invoice_no__startswith=f"INV-{year}"
                ).aggregate(Max("id"))["id__max"] or 0

                self.invoice_no = f"INV-{year}-{last_id + 1:04d}"

        self.net_amount = self.total_amount - self.discount
        self.due_amount = self.net_amount - self.paid_amount

        if self.due_amount == 0:
            self.payment_status = "PAID"
        elif self.paid_amount > 0:
            self.payment_status = "PARTIAL"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_no