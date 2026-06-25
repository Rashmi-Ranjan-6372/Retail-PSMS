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
        "plan_type",
        "monthly_price",
        "yearly_price",
        "max_users",
        "max_branches",
        "max_products",
        "is_active",
    )

    list_filter = (
        "plan_type",
        "is_active",
    )

    search_fields = (
        "name",
        "plan_type",
    )

    ordering = (
        "name",
    )


@admin.register(RetailerSubscription)
class RetailerSubscriptionAdmin(admin.ModelAdmin):

    list_display = (
        "retailer",
        "plan",
        "billing_cycle",
        "status",
        "start_date",
        "expiry_date",
        "auto_renew",
    )

    list_filter = (
        "billing_cycle",
        "status",
        "auto_renew",
    )

    search_fields = (
        "retailer__name",
        "plan__name",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "retailer",
        "amount",
        "payment_status",
        "payment_date"
    )