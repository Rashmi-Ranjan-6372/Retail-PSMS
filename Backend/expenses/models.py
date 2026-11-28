
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone


# =====================================================
# EXPENSE CATEGORY
# =====================================================

class ExpenseCategory(models.Model):

    SCOPE_CHOICES = (
        ("platform", "Platform"),
        ("retailer", "Retailer"),
    )

    scope = models.CharField(max_length=20,choices=SCOPE_CHOICES,)
    retailer = models.ForeignKey("accounts.Retailer",on_delete=models.CASCADE,related_name="expense_categories",null=True,blank=True,)
    name = models.CharField(max_length=100,)
    description = models.TextField(blank=True,null=True,)
    is_active = models.BooleanField(default=True,)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="created_expense_categories",)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["retailer", "name"],
                condition=Q(scope="retailer"),
                name="unique_retailer_expense_category",
            ),
            models.UniqueConstraint(
                fields=["name"],
                condition=Q(scope="platform"),
                name="unique_platform_expense_category",
            ),
            models.CheckConstraint(
                condition=(
                    Q(scope="platform", retailer__isnull=True)
                    | Q(scope="retailer", retailer__isnull=False)
                ),
                name="expense_category_scope_valid",
            ),
        ]

        indexes = [
            models.Index(
                fields=["scope", "is_active"],
                name="expense_cat_scope_active_idx",
            ),
        ]

    def clean(self):

        if self.scope == "platform" and self.retailer_id:
            raise ValidationError(
                "Platform categories cannot belong to a retailer."
            )

        if self.scope == "retailer" and not self.retailer_id:
            raise ValidationError(
                "Retailer categories must belong to a retailer."
            )

    def __str__(self):
        return self.name


# =====================================================
# EXPENSE
# =====================================================

class Expense(models.Model):

    SCOPE_CHOICES = (
        ("platform", "Platform"),
        ("retailer", "Retailer"),
    )

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("approved", "Approved"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    )

    PAYMENT_METHOD_CHOICES = (
        ("cash", "Cash"),
        ("upi", "UPI"),
        ("card", "Card"),
        ("bank_transfer", "Bank Transfer"),
        ("cheque", "Cheque"),
        ("other", "Other"),
    )

    scope = models.CharField(max_length=20,choices=SCOPE_CHOICES,)
    retailer = models.ForeignKey("accounts.Retailer",on_delete=models.PROTECT,related_name="expenses",null=True,blank=True,)
    branch = models.ForeignKey("branches.Branch",on_delete=models.PROTECT,related_name="expenses",null=True,blank=True,)
    category = models.ForeignKey(ExpenseCategory,on_delete=models.PROTECT,related_name="expenses",)
    expense_number = models.CharField(max_length=50,)
    title = models.CharField(max_length=200,)
    description = models.TextField(blank=True,null=True,)
    expense_date = models.DateField(default=timezone.localdate,)
    amount = models.DecimalField(max_digits=14,decimal_places=2,)
    tax_amount = models.DecimalField(max_digits=14,decimal_places=2,default=Decimal("0.00"),)
    payment_method = models.CharField(max_length=30,choices=PAYMENT_METHOD_CHOICES,default="cash",)
    payment_reference = models.CharField(max_length=150,blank=True,null=True,)
    vendor_name = models.CharField(max_length=200,blank=True,null=True,)
    invoice_number = models.CharField(max_length=100,blank=True,null=True,)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="draft",)
    notes = models.TextField(blank=True,null=True,)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name="created_expenses",)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="approved_expenses",)
    approved_at = models.DateTimeField(null=True,blank=True,)
    paid_at = models.DateTimeField(null=True,blank=True,)
    cancelled_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="cancelled_expenses",)
    cancelled_at = models.DateTimeField(null=True,blank=True,)
    cancellation_reason = models.TextField(blank=True,null=True,)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)

    class Meta:
        ordering = ["-expense_date", "-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["scope", "expense_number"],
                name="unique_expense_number_per_scope",
            ),
            models.CheckConstraint(
                condition=Q(amount__gt=0),
                name="expense_amount_positive",
            ),
            models.CheckConstraint(
                condition=Q(tax_amount__gte=0),
                name="expense_tax_non_negative",
            ),
            models.CheckConstraint(
                condition=(
                    Q(
                        scope="platform",
                        retailer__isnull=True,
                        branch__isnull=True,
                    )
                    | Q(
                        scope="retailer",
                        retailer__isnull=False,
                    )
                ),
                name="expense_scope_valid",
            ),
        ]

        indexes = [
            models.Index(
                fields=["scope", "expense_date"],
                name="expense_scope_date_idx",
            ),
            models.Index(
                fields=["retailer", "expense_date"],
                name="expense_retailer_date_idx",
            ),
            models.Index(
                fields=["branch", "expense_date"],
                name="expense_branch_date_idx",
            ),
            models.Index(
                fields=["scope", "status"],
                name="expense_scope_status_idx",
            ),
        ]

    @property
    def total_amount(self):
        return self.amount + self.tax_amount

    def clean(self):

        errors = {}

        if self.scope == "platform":

            if self.retailer_id or self.branch_id:
                errors["scope"] = (
                    "Platform expenses cannot belong to a retailer or branch."
                )

        elif self.scope == "retailer":

            if not self.retailer_id:
                errors["retailer"] = (
                    "Retailer is required for retailer expenses."
                )

            if self.branch_id and self.retailer_id:
                if self.branch.retailer_id != self.retailer_id:
                    errors["branch"] = (
                        "Branch must belong to the selected retailer."
                    )

        if self.category_id and self.scope:
            if self.category.scope != self.scope:
                errors["category"] = (
                    "Category scope must match expense scope."
                )

            elif self.scope == "retailer":
                if self.category.retailer_id != self.retailer_id:
                    errors["category"] = (
                        "Category must belong to the selected retailer."
                    )

        if self.amount is not None and self.amount <= 0:
            errors["amount"] = "Amount must be greater than zero."

        if self.tax_amount is not None and self.tax_amount < 0:
            errors["tax_amount"] = "Tax amount cannot be negative."

        if self.status == "cancelled" and not self.cancellation_reason:
            errors["cancellation_reason"] = (
                "Cancellation reason is required."
            )

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.expense_number} - {self.title}"


# =====================================================
# EXPENSE ATTACHMENT
# =====================================================

class ExpenseAttachment(models.Model):

    expense = models.ForeignKey(Expense,on_delete=models.PROTECT,related_name="attachments",)
    file = models.FileField(upload_to="expenses/attachments/%Y/%m/",)
    file_name = models.CharField(max_length=255,blank=True,)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name="uploaded_expense_attachments",)
    uploaded_at = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return self.file_name or self.file.name
