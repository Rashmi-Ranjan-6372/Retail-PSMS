
from django.db import models
from django.db.models import Q, F
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone

from accounts.models import Retailer
from branches.models import Branch

class StockBatch(models.Model):

    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="stock_batches")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="stock_batches")
    product = models.ForeignKey("masters.Product", on_delete=models.PROTECT, related_name="stock_batches")
    supplier = models.ForeignKey("masters.Supplier",on_delete=models.PROTECT,null=True,blank=True,related_name="stock_batches",)
    batch_no = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=0)
    available_qty = models.PositiveIntegerField(default=0)
    reserved_qty = models.PositiveIntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    mrp = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    expiry_date = models.DateField()
    manufacture_date = models.DateField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["expiry_date", "id"]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "retailer",
                    "branch",
                    "product",
                    "batch_no"
                ],
                name="unique_retailer_branch_product_batch"
            ),

            models.CheckConstraint(
                condition=Q(quantity__gte=0),
                name="stock_batch_quantity_nonnegative"
            ),

            models.CheckConstraint(
                condition=Q(available_qty__gte=0),
                name="stock_batch_available_nonnegative"
            ),

            models.CheckConstraint(
                condition=Q(reserved_qty__gte=0),
                name="stock_batch_reserved_nonnegative"
            ),

            models.CheckConstraint(
                condition=Q(
                    available_qty__lte=F("quantity")
                ),
                name="stock_batch_available_lte_quantity"
            ),

            models.CheckConstraint(
                condition=Q(
                    reserved_qty__lte=F("quantity")
                ),
                name="stock_batch_reserved_lte_quantity"
            ),

            models.CheckConstraint(
                condition=Q(
                    available_qty__lte=(
                        F("quantity") - F("reserved_qty")
                    )
                ),
                name="stock_batch_available_reserved_lte_quantity"
            ),

            models.CheckConstraint(
                condition=Q(
                    sale_price__lte=F("mrp")
                ),
                name="stock_batch_sale_price_lte_mrp"
            ),

            models.CheckConstraint(
                condition=(
                    Q(manufacture_date__isnull=True)
                    | Q(manufacture_date__lte=F("expiry_date"))
                ),
                name="stock_batch_manufacture_before_expiry"
            ),
        ]

        indexes = [
            models.Index(
                fields=["retailer", "branch", "product"]
            ),
            models.Index(
                fields=["retailer", "branch", "expiry_date"]
            ),
            models.Index(
                fields=["retailer", "product", "available_qty"]
            ),
            models.Index(fields=["batch_no"]),
            models.Index(fields=["is_expired"]),
        ]

    def clean(self):

        super().clean()

        errors = {}

        if self.branch_id and self.retailer_id:

            if self.branch.retailer_id != self.retailer_id:
                errors["branch"] = (
                    "Branch does not belong to this retailer."
                )

        if self.product_id and self.retailer_id:

            if self.product.retailer_id != self.retailer_id:
                errors["product"] = (
                    "Product does not belong to this retailer."
                )

        if self.supplier_id and self.retailer_id:

            if self.supplier.retailer_id != self.retailer_id:
                errors["supplier"] = (
                    "Supplier does not belong to this retailer."
                )

        if (
            self.manufacture_date
            and self.expiry_date
            and self.manufacture_date > self.expiry_date
        ):
            errors["manufacture_date"] = (
                "Manufacture date cannot be after expiry date."
            )

        if (
            self.available_qty is not None
            and self.reserved_qty is not None
            and self.quantity is not None
        ):

            if self.available_qty + self.reserved_qty > self.quantity:
                errors["available_qty"] = (
                    "Available and reserved stock cannot exceed total quantity."
                )

        if (
            self.sale_price is not None
            and self.mrp is not None
            and self.sale_price > self.mrp
        ):
            errors["sale_price"] = (
                "Sale price cannot exceed MRP."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):

        if self.expiry_date:
            self.is_expired = (
                self.expiry_date < timezone.localdate()
            )

        update_fields = kwargs.get("update_fields")

        if update_fields is not None:
            kwargs["update_fields"] = (
                set(update_fields) | {"is_expired"}
            )

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.product.name} - {self.batch_no}"
