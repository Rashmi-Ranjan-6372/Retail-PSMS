from django.db import models
from accounts.models import Retailer
from branches.models import Branch

class Customer(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="customers")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="customers")
    name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "customers"

        ordering = ["-id"]

        unique_together = [
            ("retailer", "mobile")
        ]

    def __str__(self):
        return f"{self.name} ({self.mobile})"