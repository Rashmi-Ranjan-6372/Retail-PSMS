from django.db import models
from .constants import ADJUSTMENT_TYPE
from django.conf import settings

class StockTransactionItem(models.Model):
    transaction = models.ForeignKey("StockTransaction", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("masters.Product", on_delete=models.CASCADE)
    batch = models.ForeignKey("inventory.StockBatch", on_delete=models.CASCADE)
    branch = models.ForeignKey("branches.Branch", on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPE)

    qty = models.PositiveIntegerField()
    free_qty = models.PositiveIntegerField(default=0)

    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    available_after = models.IntegerField(default=0)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.qty * self.purchase_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} ({self.movement_type})"