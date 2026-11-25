
from django.db import models
from .products_category_models import Category
from .manufacturers_models import Manufacturer
from accounts.models import Retailer


class Product(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, related_name="products")
    strength = models.CharField(max_length=100, blank=True, default="", help_text="Example: 500mg, 650mg")
    prescription_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["retailer", "name", "manufacturer", "strength"],
                name="unique_product_per_retailer"
            )
        ]
        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        if self.strength:
            return f"{self.name} {self.strength}"
        return self.name
