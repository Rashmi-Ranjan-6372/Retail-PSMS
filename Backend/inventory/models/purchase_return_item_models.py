from django.db import models
from .constants import RETURN_TYPE
from django.conf import settings

class PurchaseReturnItem(models.Model):

    purchase_return = models.ForeignKey("PurchaseReturn", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("masters.Product", on_delete=models.CASCADE)
    batch = models.ForeignKey("inventory.StockBatch", on_delete=models.CASCADE)

    qty = models.IntegerField()
    free_qty = models.IntegerField(default=0)

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    return_type = models.CharField(max_length=20, choices=RETURN_TYPE, default="GOOD")
    remarks = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.amount = self.qty * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} ({self.qty})"