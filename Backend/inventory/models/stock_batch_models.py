from django.db import models
from django.conf import settings
from accounts.models import Retailer
from branches.models import Branch
from django.utils.timezone import now
class StockBatch(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="stock_batches")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="stock_batches")
    product = models.ForeignKey("masters.Product", on_delete=models.CASCADE)
    supplier = models.ForeignKey("masters.Supplier", on_delete=models.SET_NULL, null=True, blank=True)
    batch_no = models.CharField(max_length=50)

    quantity = models.IntegerField(default=0)
    available_qty = models.IntegerField(default=0)
    reserved_qty = models.IntegerField(default=0)

    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    expiry_date = models.DateField()
    manufacture_date = models.DateField(null=True, blank=True)

    is_expired = models.BooleanField(default=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["expiry_date"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["product"]),
            models.Index(fields=["supplier"]),
            models.Index(fields=["batch_no"]),
            models.Index(fields=["expiry_date"]),
            models.Index(fields=["is_expired"]),
        ]

        unique_together = [
            ("product", "batch_no", "branch")
        ]

    # =========================
    # AUTO AVAILABLE QTY
    # =========================

    def save(self, *args, **kwargs):

        if self.available_qty is None:
            self.available_qty = self.quantity

        if self.expiry_date:
            self.is_expired = (
                self.expiry_date < now().date()
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.product.name} - "
            f"{self.batch_no}"
        )