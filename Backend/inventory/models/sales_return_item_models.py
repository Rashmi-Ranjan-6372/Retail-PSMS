from django.db import models
from django.conf import settings
from accounts.models import Retailer
from branches.models import Branch

class SalesReturnItem(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="sales_return_items")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales_return_items")
    sales_return = models.ForeignKey("SalesReturn", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("masters.Product", on_delete=models.CASCADE)
    batch = models.ForeignKey("inventory.StockBatch", on_delete=models.CASCADE)
    qty = models.IntegerField()
    free_qty = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reason = models.CharField(max_length=255, null=True, blank=True)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:

        ordering = ["-id"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["product"]),
            models.Index(fields=["batch"]),
            models.Index(fields=["created_at"]),
        ]

    def save(self, *args, **kwargs):

        base_amount = (
            (self.qty or 0) *
            (self.unit_price or 0)
        )

        self.amount = (
            base_amount -
            (self.discount or 0)
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.product.name} ({self.qty})"