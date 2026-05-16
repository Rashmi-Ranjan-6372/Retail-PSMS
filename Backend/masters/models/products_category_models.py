from django.db import models
from accounts.models import Retailer
from branches.models import Branch

class Category(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="categories")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="categories")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"

        ordering = ["name"]

        unique_together = [
            ("retailer", "name"),
            ("retailer", "code"),
        ]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
            models.Index(fields=["is_active"]),
        ]

    def save(self, *args, **kwargs):

        if self.code:
            self.code = self.code.upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name