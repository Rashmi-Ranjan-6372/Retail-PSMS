from django.db import models
from accounts.models import Retailer
from branches.models import Branch

class Manufacturer(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="manufacturers")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="manufacturers")
    name = models.CharField(max_length=255)
    gst_no = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "manufacturers"

        ordering = ["name"]

        unique_together = [
            ("retailer", "name")
        ]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name