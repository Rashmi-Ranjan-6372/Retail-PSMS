from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

from accounts.models import Retailer
from branches.models import Branch

from .constants import DISCOUNT_TYPE


class SalesReturnItem(models.Model):

    retailer = models.ForeignKey(Retailer,on_delete=models.CASCADE, related_name="sales_return_items")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales_return_items")
    sales_return = models.ForeignKey("SalesReturn", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("masters.Product", on_delete=models.CASCADE)
    batch = models.ForeignKey("inventory.StockBatch", on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
    free_qty = models.PositiveIntegerField( default=0)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0)
        ]
    )
    discount_type = models.CharField(max_length=20,choices=DISCOUNT_TYPE, default="FLAT")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0,
        validators=[
            MinValueValidator(0)
        ]
    )

    reason = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-id"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["product"]),
            models.Index(fields=["batch"]),
            models.Index(fields=["discount_type"]),
            models.Index(fields=["created_at"]),

            models.Index(
                fields=["retailer", "branch"]
            ),

            models.Index(
                fields=["retailer", "product"]
            ),

            models.Index(
                fields=["branch", "product"]
            ),

            models.Index(
                fields=["sales_return"]
            ),

            models.Index(
                fields=["sales_return", "product"]
            ),

            models.Index(
                fields=["product", "batch"]
            ),
        ]

    def save(self, *args, **kwargs):

        if self.qty <= 0:
            raise ValueError(
                "Quantity must be greater than 0"
            )

        if self.free_qty < 0:
            raise ValueError(
                "Free quantity cannot be negative"
            )

        if self.unit_price < 0:
            raise ValueError(
                "Unit price cannot be negative"
            )

        if self.discount < 0:
            raise ValueError(
                "Discount cannot be negative"
            )

        base_amount = (
            self.qty *
            self.unit_price
        )

        if self.discount_type == "FLAT":

            if self.discount > base_amount:
                raise ValueError(
                    "Flat discount cannot exceed amount"
                )

            discount_amount = self.discount

        elif self.discount_type == "PERCENTAGE":

            if self.discount > 100:
                raise ValueError(
                    "Discount percentage cannot exceed 100"
                )

            discount_amount = (
                base_amount *
                self.discount
            ) / 100

        else:

            raise ValueError(
                "Invalid discount type"
            )

        self.amount = (
            base_amount -
            discount_amount
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.product.name} ({self.qty})"