from django.contrib import admin
from .models import (
    SubscriptionPlan,
    RetailerSubscription,
    PaymentHistory
)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "monthly_price",
        "yearly_price",
        "max_users",
        "max_branches",
        "is_active"
    )


@admin.register(RetailerSubscription)
class RetailerSubscriptionAdmin(admin.ModelAdmin):

    list_display = (
        "retailer",
        "plan",
        "status",
        "start_date",
        "expiry_date"
    )


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "retailer",
        "amount",
        "payment_status",
        "payment_date"
    )