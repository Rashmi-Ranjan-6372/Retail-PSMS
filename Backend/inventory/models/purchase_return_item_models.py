from django.db import models
from .constants import RETURN_TYPE
from django.conf import settings
from accounts.models import Retailer
from branches.models import Branch

class PurchaseReturnItem(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="purchase_return_items")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="purchase_return_items")
    purchase_return = models.ForeignKey("PurchaseReturn", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("masters.Product", on_delete=models.CASCADE)
    batch = models.ForeignKey("inventory.StockBatch", on_delete=models.CASCADE)

    qty = models.IntegerField()
    free_qty = models.IntegerField(default=0)

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    return_type = models.CharField(max_length=20, choices=RETURN_TYPE, default="GOOD")
    remarks = models.TextField(null=True, blank=True)
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
            models.Index(fields=["return_type"]),
        ]

    def save(self, *args, **kwargs):

        self.amount = (
            self.qty * self.unit_price
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.product.name} "
            f"({self.qty})"
        )