from django.db import models
from django.db.models import Max
from datetime import datetime
from django.db import transaction
from .constants import STATUS
from django.conf import settings

class SalesReturn(models.Model):
    return_no = models.CharField(max_length=50, unique=True, blank=True)
    sales = models.ForeignKey("Sales", on_delete=models.CASCADE)
    branch = models.ForeignKey("branches.Branch", on_delete=models.CASCADE)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS, default="COMPLETED")
    remarks = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.return_no:
            year = datetime.now().year

            with transaction.atomic():
                last_id = SalesReturn.objects.filter(
                    return_no__startswith=f"SR-{year}"
                ).aggregate(Max("id"))["id__max"] or 0

                self.return_no = f"SR-{year}-{last_id + 1:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.return_no