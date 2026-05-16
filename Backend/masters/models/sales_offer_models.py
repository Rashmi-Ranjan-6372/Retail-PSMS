from django.db import models
from .products_models import Product
from .products_category_models import Category
from .manufacturers_models import Manufacturer
from accounts.models import Retailer
from branches.models import Branch
from django.core.exceptions import ValidationError
from django.utils import timezone

class SalesOffer(models.Model):
    OFFER_TYPE_CHOICES = [
        ("PRODUCT_DISCOUNT", "Product Discount"),
        ("CATEGORY_DISCOUNT", "Category Discount"),
        ("BUY_X_GET_Y", "Buy X Get Y"),
        ("QUANTITY_DISCOUNT", "Quantity Discount"),
        ("FLAT_DISCOUNT", "Flat Discount"),
        ("BILL_AMOUNT_DISCOUNT", "Bill Amount Discount"),
        ("MANUFACTURER_DISCOUNT", "Manufacturer Discount"),
        ("EXPIRY_CLEARANCE", "Expiry Clearance"),
        ("FESTIVAL_OFFER", "Festival Offer"),
        ("MEMBER_DISCOUNT", "Member Discount"),
    ]
    DISCOUNT_TYPE_CHOICES = [("PERCENTAGE", "Percentage"), ("FLAT", "Flat")]
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="sales_offers")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales_offers")
    name = models.CharField(max_length=255)
    offer_type = models.CharField(max_length=30, choices=OFFER_TYPE_CHOICES)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default="PERCENTAGE")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="offers", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="offers", blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="offers", blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    flat_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    buy_quantity = models.PositiveIntegerField(blank=True, null=True)
    free_quantity = models.PositiveIntegerField(blank=True, null=True)
    minimum_quantity = models.PositiveIntegerField(blank=True, null=True)
    minimum_bill_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    expiry_before_days = models.PositiveIntegerField(blank=True, null=True)
    member_type = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        db_table = "sales_offers"

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["offer_type"]),
            models.Index(fields=["start_date"]),
            models.Index(fields=["end_date"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name

    @property
    def is_valid_offer(self):

        today = timezone.now().date()

        return (
            self.is_active and
            self.start_date <= today <= self.end_date
        )

    def clean(self):

        if self.start_date > self.end_date:
            raise ValidationError(
                "Start date cannot be greater than end date"
            )

        if (
            self.discount_type == "PERCENTAGE" and
            self.discount_percentage is None
        ):
            raise ValidationError(
                "Discount percentage is required"
            )

        if (
            self.discount_type == "FLAT" and
            self.flat_discount_amount is None
        ):
            raise ValidationError(
                "Flat discount amount is required"
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)
        
        