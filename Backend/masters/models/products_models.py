from django.db import models
from .products_category_models import Category
from .manufacturers_models import Manufacturer
from accounts.models import Retailer
from branches.models import Branch

class Product(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="products")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name="products")
    manufacturer = models.ForeignKey(Manufacturer,on_delete=models.PROTECT,related_name="products")
    strength = models.CharField(max_length=100,blank=True,null=True,help_text="Example: 500mg, 650mg")
    units_per_strip = models.PositiveIntegerField(default=1,help_text="Example: 10 tablets in 1 strip")
    loose_sale_allowed = models.BooleanField(default=True)
    prescription_required = models.BooleanField(default=False)
    rack_no = models.CharField(max_length=50,blank=True,null=True)
    minimum_stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    deleted_at = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        ordering = ["name"]
        unique_together = [
            (
                "retailer",
                "name",
                "manufacturer",
                "strength"
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