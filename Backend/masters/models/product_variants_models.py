from django.db import models
from django.core.validators import MinValueValidator
from .products_models import Product


class ProductVariant(models.Model):
    product = models.ForeignKey(Product,on_delete=models.PROTECT,related_name="variants")
    variant_name = models.CharField(max_length=100)
    units_per_pack = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)])
    loose_sale_allowed = models.BooleanField(default=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product_variants"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "variant_name"],
                name="unique_variant_name_per_product"
            )
        ]

    def __str__(self):
        return f"{self.product.name} - {self.variant_name}"