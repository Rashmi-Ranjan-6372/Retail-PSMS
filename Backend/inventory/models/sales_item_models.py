from django.db import models
from accounts.models import Retailer
from branches.models import Branch
from django.conf import settings

class SalesItem(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="sales_items")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales_items")
    sales = models.ForeignKey("Sales",on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey("masters.Product",on_delete=models.CASCADE)
    batch = models.ForeignKey("inventory.StockBatch",on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    free_qty = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    tax_percent = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    tax_amount = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    amount = models.DecimalField(max_digits=12,decimal_places=2,default=0)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-id"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["sales"]),
            models.Index(fields=["product"]),
            models.Index(fields=["batch"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["retailer", "branch"]),
            models.Index(fields=["retailer", "sales"]),
            models.Index(fields=["retailer", "product"]),
            models.Index(fields=["branch", "product"]),
            models.Index(fields=["sales", "product"]),
            models.Index(fields=["product", "batch"]),
        ]

    # =========================
    # AUTO CALCULATE AMOUNT
    # =========================

    def save(self, *args, **kwargs):

        if self.qty <= 0:
            raise ValueError(
                "Quantity must be greater than 0"
            )

        if self.unit_price < 0:
            raise ValueError(
                "Unit price cannot be negative"
            )

        if self.discount < 0:
            raise ValueError(
                "Discount cannot be negative"
            )

        if self.tax_percent < 0:
            raise ValueError(
                "Tax percent cannot be negative"
            )

        base_amount = (
            (self.qty or 0) *
            (self.unit_price or 0)
        )

        discounted_amount = (
            base_amount - (self.discount or 0)
        )

        if discounted_amount < 0:
            discounted_amount = 0

        self.tax_amount = (
            discounted_amount *
            (self.tax_percent or 0)
        ) / 100

        self.amount = (
            discounted_amount +
            self.tax_amount
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.product.name} ({self.qty})"