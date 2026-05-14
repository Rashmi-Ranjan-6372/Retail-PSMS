from django.db import models
from django.conf import settings

class StockBatch(models.Model):
    product = models.ForeignKey("masters.Product", on_delete=models.CASCADE)
    branch = models.ForeignKey("branches.Branch", on_delete=models.CASCADE)

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

    def save(self, *args, **kwargs):

        # Keep available stock safe
        if self.available_qty is None:
            self.available_qty = self.quantity

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.batch_no}"