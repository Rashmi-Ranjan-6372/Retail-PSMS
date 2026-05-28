from django.db import models
from django.conf import settings
from accounts.models import Retailer
from branches.models import Branch


class FinancialYear(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="financial_years")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="financial_years")
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-id"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["start_date"]),
            models.Index(fields=["end_date"]),
            models.Index(fields=["retailer", "branch"]),
        ]

        unique_together = (
            "retailer",
            "name",
        )

    def save(self, *args, **kwargs):

        if self.start_date >= self.end_date:

            raise ValueError(
                "End date must be greater than start date"
            )

        if self.is_active:

            FinancialYear.objects.filter(
                retailer=self.retailer,
                is_active=True
            ).exclude(
                id=self.id
            ).update(
                is_active=False
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.name}"
        )