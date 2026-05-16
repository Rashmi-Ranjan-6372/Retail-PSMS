from django.db import models
from branches.models import Branch
from accounts.models import Retailer
from branches.models import Branch

class Supplier(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="suppliers")
    branches = models.ManyToManyField(Branch, related_name="suppliers")
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gst_no = models.CharField(max_length=20, blank=True, null=True, unique=True)
    drug_license_no = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["gst_no"]),
            models.Index(fields=["is_active"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["retailer", "phone"],
                name="unique_supplier_phone_per_retailer"
            ),

            models.UniqueConstraint(
                fields=["retailer", "gst_no"],
                name="unique_supplier_gst_per_retailer"
            ),
        ]