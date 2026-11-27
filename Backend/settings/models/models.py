
from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError

from accounts.models import Retailer
from branches.models import Branch


class GeneralSetting(models.Model):

    retailer = models.OneToOneField(Retailer,on_delete=models.CASCADE,related_name="general_setting")
    currency = models.CharField(max_length=10,default="INR")
    timezone = models.CharField(max_length=100,default="Asia/Kolkata")
    low_stock_limit = models.PositiveIntegerField(default=10)
    enable_gst = models.BooleanField(default=True)
    enable_barcode = models.BooleanField(default=True)
    enable_expiry_alert = models.BooleanField(default=True)
    enable_loose_sale = models.BooleanField(default=True)
    enable_negative_stock = models.BooleanField(default=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="created_general_settings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.retailer.name} Settings"


class FinancialYear(models.Model):

    retailer = models.ForeignKey(Retailer,on_delete=models.CASCADE,related_name="financial_years")
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True,blank=True,related_name="financial_years")
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    remarks = models.TextField(null=True,blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="created_financial_years")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-id"]

        indexes = [
            models.Index(
                fields=["retailer", "branch"],
                name="fy_retailer_branch_idx"
            ),
            models.Index(
                fields=["retailer", "is_active"],
                name="fy_retailer_active_idx"
            ),
            models.Index(
                fields=["start_date", "end_date"],
                name="fy_date_range_idx"
            ),
        ]

        constraints = [

            # One financial year name per retailer-wide scope.
            models.UniqueConstraint(
                fields=["retailer", "name"],
                condition=models.Q(branch__isnull=True),
                name="unique_retailer_financial_year"
            ),

            # One financial year name per branch.
            models.UniqueConstraint(
                fields=["retailer", "branch", "name"],
                condition=models.Q(branch__isnull=False),
                name="unique_branch_financial_year"
            ),

            # Only one active retailer-wide financial year.
            models.UniqueConstraint(
                fields=["retailer"],
                condition=models.Q(
                    branch__isnull=True,
                    is_active=True
                ),
                name="unique_active_retailer_financial_year"
            ),

            # Only one active financial year per branch.
            models.UniqueConstraint(
                fields=["retailer", "branch"],
                condition=models.Q(
                    branch__isnull=False,
                    is_active=True
                ),
                name="unique_active_branch_financial_year"
            ),
        ]

    def clean(self):

        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError({
                    "end_date": "End date must be greater than start date."
                })

        if self.branch_id and self.retailer_id:
            if self.branch.retailer_id != self.retailer_id:
                raise ValidationError({
                    "branch": "Selected branch does not belong to this retailer."
                })

    def save(self, *args, **kwargs):

        self.full_clean()

        with transaction.atomic():

            if self.is_active:

                queryset = FinancialYear.objects.filter(
                    retailer_id=self.retailer_id,
                    branch_id=self.branch_id,
                    is_active=True
                )

                if self.pk:
                    queryset = queryset.exclude(pk=self.pk)

                queryset.update(is_active=False)

            super().save(*args, **kwargs)

    def __str__(self):
        scope = self.branch.name if self.branch_id else "All Branches"
        return f"{self.name} | {scope}"
