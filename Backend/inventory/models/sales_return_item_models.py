from decimal import Decimal

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import Q

from accounts.models import Retailer
from branches.models import Branch

from .constants import DISCOUNT_TYPE


class SalesReturnItem(models.Model):

    retailer = models.ForeignKey(Retailer, on_delete=models.PROTECT, related_name="sales_return_items")
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True,blank=True,related_name="sales_return_items",)
    sales_return = models.ForeignKey("SalesReturn", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("masters.Product", on_delete=models.PROTECT, related_name="sales_return_items")
    batch = models.ForeignKey("inventory.StockBatch",on_delete=models.PROTECT,related_name="sales_return_items",)
    qty = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    free_qty = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE, default="FLAT")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
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
            models.Index(fields=["retailer", "branch"]),
            models.Index(fields=["retailer", "product"]),
            models.Index(fields=["branch", "product"]),
            models.Index(fields=["sales_return"]),
            models.Index(fields=["sales_return", "product"]),
            models.Index(fields=["product", "batch"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(qty__gte=1), name="sales_return_item_qty_positive"
            ),
            models.CheckConstraint(
                condition=Q(free_qty__gte=0),
                name="sales_return_item_free_qty_nonnegative",
            ),
            models.CheckConstraint(
                condition=Q(unit_price__gte=0),
                name="sales_return_item_unit_price_nonnegative",
            ),
            models.CheckConstraint(
                condition=Q(discount__gte=0),
                name="sales_return_item_discount_nonnegative",
            ),
            models.CheckConstraint(
                condition=Q(amount__gte=0), name="sales_return_item_amount_nonnegative"
            ),
        ]

    def clean(self):
        super().clean()

        if self.qty is not None and self.qty <= 0:
            raise ValidationError({"qty": "Return quantity must be greater than zero."})

        if self.free_qty is not None and self.free_qty < 0:
            raise ValidationError({"free_qty": "Free quantity cannot be negative."})

        if self.unit_price is not None and self.unit_price < 0:
            raise ValidationError({"unit_price": "Unit price cannot be negative."})

        if self.discount is not None and self.discount < 0:
            raise ValidationError({"discount": "Discount cannot be negative."})

        if self.discount_type not in dict(DISCOUNT_TYPE):
            raise ValidationError({"discount_type": "Invalid discount type."})

        if self.sales_return_id:
            if self.sales_return.retailer_id != self.retailer_id:
                raise ValidationError(
                    {"sales_return": "Sales return does not belong to this retailer."}
                )

            if self.sales_return.branch_id != self.branch_id:
                raise ValidationError(
                    {"branch": "Branch does not match the selected sales return."}
                )

        if self.branch_id and self.branch.retailer_id != self.retailer_id:
            raise ValidationError(
                {"branch": "Selected branch does not belong to this retailer."}
            )

        if self.product_id:
            if self.product.retailer_id != self.retailer_id:
                raise ValidationError(
                    {"product": "Selected product does not belong to this retailer."}
                )

        if self.batch_id:
            if self.batch.retailer_id != self.retailer_id:
                raise ValidationError(
                    {"batch": "Selected batch does not belong to this retailer."}
                )

            if self.batch.product_id != self.product_id:
                raise ValidationError(
                    {"batch": "Selected batch does not belong to this product."}
                )

            if self.batch.branch_id != self.branch_id:
                raise ValidationError(
                    {"batch": "Selected batch does not belong to this branch."}
                )

    def save(self, *args, **kwargs):

        if self.qty is None or self.qty <= 0:
            raise ValidationError("Return quantity must be greater than zero.")

        if self.free_qty is None or self.free_qty < 0:
            raise ValidationError("Free quantity cannot be negative.")

        if self.unit_price is None or self.unit_price < 0:
            raise ValidationError("Unit price cannot be negative.")

        if self.discount is None or self.discount < 0:
            raise ValidationError("Discount cannot be negative.")

        base_amount = Decimal(self.qty) * self.unit_price

        if self.discount_type == "FLAT":

            if self.discount > base_amount:
                raise ValidationError("Flat discount cannot exceed base amount.")

            discount_amount = self.discount

        elif self.discount_type == "PERCENTAGE":

            if self.discount > 100:
                raise ValidationError("Discount percentage cannot exceed 100.")

            discount_amount = (base_amount * self.discount) / Decimal("100")

        else:
            raise ValidationError("Invalid discount type.")

        self.amount = base_amount - discount_amount

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} ({self.qty})"
