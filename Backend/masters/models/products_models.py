from django.db import models
from .products_category_models import Category
from .manufacturers_models import Manufacturer


class Product(models.Model):
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

        indexes = [
            models.Index(fields=["name"]),
        ]

        unique_together = [
            ("name", "manufacturer", "strength")
        ]