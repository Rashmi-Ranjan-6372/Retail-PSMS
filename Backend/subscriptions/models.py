from decimal import Decimal

from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone

from accounts.models import Retailer


# ==========================================================
# SUBSCRIPTION PLAN
# ==========================================================

class SubscriptionPlan(models.Model):

    PLAN_TYPES = (
        ("trial", "Trial"),
        ("starter", "Starter"),
        ("professional", "Professional"),
        ("enterprise", "Enterprise"),
    )

    name = models.CharField(max_length=50,unique=True)
    plan_type = models.CharField(max_length=20,choices=PLAN_TYPES)
    monthly_price = models.DecimalField(max_digits=10,decimal_places=2,default=Decimal("0.00"),validators=[MinValueValidator(Decimal("0.00"))])
    yearly_price = models.DecimalField(max_digits=10,decimal_places=2,default=Decimal("0.00"),validators=[MinValueValidator(Decimal("0.00"))])
    max_users = models.PositiveIntegerField(default=0,help_text="Maximum users allowed. 0 means unlimited.")
    max_branches = models.PositiveIntegerField(default=0,help_text="Maximum branches allowed. 0 means unlimited.")
    max_products = models.PositiveIntegerField(default=1000,help_text="Maximum products allowed. 0 means unlimited.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):

        super().clean()

        if self.monthly_price < 0:
            raise ValidationError({
                "monthly_price": "Monthly price cannot be negative."
            })

        if self.yearly_price < 0:
            raise ValidationError({
                "yearly_price": "Yearly price cannot be negative."
            })

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return self.name

    class Meta:

        ordering = ["name"]

        constraints = [
            models.CheckConstraint(
                condition=Q(monthly_price__gte=0),
                name="subscription_plan_monthly_price_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(yearly_price__gte=0),
                name="subscription_plan_yearly_price_nonnegative"
            ),
        ]


# ==========================================================
# RETAILER SUBSCRIPTION
# ==========================================================

class RetailerSubscription(models.Model):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("expired", "Expired"),
        ("suspended", "Suspended"),
    )

    BILLING_CYCLE_CHOICES = (
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    )

    retailer = models.OneToOneField(Retailer,on_delete=models.PROTECT,related_name="subscription")
    plan = models.ForeignKey(SubscriptionPlan,on_delete=models.PROTECT,related_name="subscriptions")
    billing_cycle = models.CharField(max_length=10,choices=BILLING_CYCLE_CHOICES,default="monthly")
    start_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="active")
    auto_renew = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(blank=True,null=True)
    cancelled_reason = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ------------------------------------------------------
    # DATE VALIDATION
    # ------------------------------------------------------

    def clean(self):

        super().clean()

        if self.start_date and self.expiry_date:

            if self.start_date >= self.expiry_date:

                raise ValidationError({
                    "expiry_date": "Expiry date must be after start date."
                })

    # ------------------------------------------------------
    # SUBSCRIPTION STATUS METHODS
    # ------------------------------------------------------

    def is_expired(self):

        return self.expiry_date < timezone.localdate()

    def is_active(self):

        today = timezone.localdate()

        return (
            self.status == "active"
            and self.start_date <= today
            and self.expiry_date >= today
        )

    def is_upcoming(self):

        return self.start_date > timezone.localdate()

    # ------------------------------------------------------
    # SUBSCRIPTION AMOUNT
    # ------------------------------------------------------

    @property
    def amount(self):

        if self.billing_cycle == "yearly":

            return self.plan.yearly_price

        return self.plan.monthly_price

    # ------------------------------------------------------
    # SAVE
    # ------------------------------------------------------

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.retailer.name} - "
            f"{self.plan.name} "
            f"({self.billing_cycle})"
        )

    class Meta:

        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["status"],
                name="ret_sub_status_idx"
            ),
            models.Index(
                fields=["expiry_date"],
                name="ret_sub_expiry_idx"
            ),
            models.Index(
                fields=["billing_cycle"],
                name="ret_sub_billing_idx"
            ),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(expiry_date__gt=models.F("start_date")),
                name="retailer_subscription_valid_dates"
            ),
        ]


# ==========================================================
# PAYMENT HISTORY
# ==========================================================

class PaymentHistory(models.Model):

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    retailer = models.ForeignKey(Retailer,on_delete=models.PROTECT,related_name="subscription_payments")
    subscription = models.ForeignKey(RetailerSubscription,on_delete=models.PROTECT,related_name="payment_history")
    amount = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(Decimal("0.00"))])
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS,default="pending")
    transaction_id = models.CharField(max_length=255,blank=True,null=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    # ------------------------------------------------------
    # PAYMENT VALIDATION
    # ------------------------------------------------------

    def clean(self):

        super().clean()

        if self.amount is not None and self.amount < 0:

            raise ValidationError({
                "amount": "Payment amount cannot be negative."
            })

        if self.retailer_id and self.subscription_id:

            if self.retailer_id != self.subscription.retailer_id:

                raise ValidationError({
                    "retailer": (
                        "The selected subscription does not belong "
                        "to this retailer."
                    )
                })

    # ------------------------------------------------------
    # SAVE
    # ------------------------------------------------------

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.retailer.name} - "
            f"₹{self.amount} - "
            f"{self.payment_status}"
        )

    class Meta:

        ordering = ["-payment_date"]

        indexes = [
            models.Index(
                fields=["payment_status"],
                name="payment_status_idx"
            ),
            models.Index(
                fields=["transaction_id"],
                name="payment_transaction_idx"
            ),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(amount__gte=0),
                name="payment_history_amount_nonnegative"
            ),

            models.UniqueConstraint(
                fields=["transaction_id"],
                condition=(
                    Q(transaction_id__isnull=False)
                    & ~Q(transaction_id="")
                ),
                name="unique_payment_transaction_id"
            ),
        ]