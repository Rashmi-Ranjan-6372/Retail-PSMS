from django.db import models
from django.utils import timezone
from accounts.models import Retailer


class SubscriptionPlan(models.Model):

    PLAN_TYPES = (
        ("trial", "Trial"),
        ("starter", "Starter"),
        ("professional", "Professional"),
        ("enterprise", "Enterprise"),
    )

    name = models.CharField(max_length=50, unique=True)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    yearly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_users = models.PositiveIntegerField()
    max_branches = models.PositiveIntegerField()
    max_products = models.PositiveIntegerField(default=1000)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class RetailerSubscription(models.Model):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("expired", "Expired"),
        ("suspended", "Suspended"),
    )

    retailer = models.OneToOneField(Retailer, on_delete=models.CASCADE, related_name="subscription")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    auto_renew = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        return self.expiry_date < timezone.now().date()

    def __str__(self):
        return f"{self.retailer.name} - {self.plan.name}"

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["plan"]),
            models.Index(fields=["status"]),
            models.Index(fields=["expiry_date"]),
        ]


class PaymentHistory(models.Model):

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="subscription_payments")
    subscription = models.ForeignKey(RetailerSubscription, on_delete=models.CASCADE, related_name="payment_history")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.retailer.name} - ₹{self.amount}"

    class Meta:
        ordering = ["-payment_date"]

        indexes = [
            models.Index(fields=["retailer"]),
            models.Index(fields=["payment_status"]),
            models.Index(fields=["transaction_id"]),
        ]