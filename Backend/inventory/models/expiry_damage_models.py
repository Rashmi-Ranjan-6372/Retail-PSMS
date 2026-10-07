from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

from accounts.models import Retailer
from branches.models import Branch

from .constants import STOCK_ISSUE_REASON


class ExpiryDamage(models.Model):

    retailer = models.ForeignKey(Retailer,on_delete=models.CASCADE,related_name="expiry_damages")
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True,blank=True,related_name="expiry_damages")
    product = models.ForeignKey("masters.Product", on_delete=models.CASCADE, related_name="expiry_damages")
    batch = models.ForeignKey("inventory.StockBatch", on_delete=models.CASCADE, related_name="expiry_damages")
    issue_type = models.CharField( max_length=20, choices=STOCK_ISSUE_REASON)
    quantity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    total_loss = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    expiry_date = models.DateField(null=True,blank=True)
    remarks = models.TextField(null=True,blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="created_expiry_damages")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["product"]),
            models.Index(fields=["batch"]),
            models.Index(fields=["issue_type"]),
            models.Index(fields=["expiry_date"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["retailer", "branch"]),
            models.Index(fields=["retailer", "issue_type"]),
            models.Index(fields=["retailer", "expiry_date"]),
            models.Index(fields=["branch", "issue_type"]),
        ]

    def save(self, *args, **kwargs):

        self.total_loss = (
            self.quantity * self.unit_price
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.product.name} - "
            f"{self.issue_type}"
        )