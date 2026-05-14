from django.db import models
from .constants import ADJUSTMENT_TYPE
from django.conf import settings

class StockAdjustment(models.Model):
    product = models.ForeignKey("masters.Product", on_delete=models.CASCADE)
    batch = models.ForeignKey("inventory.StockBatch", on_delete=models.CASCADE)
    branch = models.ForeignKey("branches.Branch", on_delete=models.CASCADE)

    adjustment_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPE)

    adjustment_qty = models.IntegerField()

    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    reason = models.CharField(max_length=255)
    remarks = models.TextField(null=True, blank=True)

    reference_no = models.CharField(max_length=50, null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_value = self.adjustment_qty * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} ({self.adjustment_type})"