from django.db import models


class SalesReturnItem(models.Model):

    sales_return = models.ForeignKey("SalesReturn", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("masters.Product", on_delete=models.CASCADE)
    batch = models.ForeignKey("inventory.StockBatch", on_delete=models.CASCADE)

    qty = models.IntegerField()
    free_qty = models.IntegerField(default=0)

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    reason = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        base = self.qty * self.unit_price
        self.amount = base - self.discount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} ({self.qty})"