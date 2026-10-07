from django.contrib import admin

from .models import (
    SubscriptionPlan,
    RetailerSubscription,
    PaymentHistory,
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
        "created_at",
    )

    list_filter = (
        "plan_type",
        "is_active",
    )

    search_fields = (
        "name",
        "plan_type",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("name",)


@admin.register(RetailerSubscription)
class RetailerSubscriptionAdmin(admin.ModelAdmin):

    list_display = (
        "retailer",
        "plan",
        "billing_cycle",
        "start_date",
        "expiry_date",
        "status",
        "auto_renew",
        "created_at",
    )

    list_filter = (
        "status",
        "billing_cycle",
        "auto_renew",
        "plan",
    )

    search_fields = (
        "retailer__name",
        "plan__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "retailer",
        "plan",
    )

    ordering = ("-created_at",)


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "retailer",
        "subscription",
        "amount",
        "payment_status",
        "transaction_id",
        "payment_date",
    )

    list_filter = (
        "payment_status",
        "payment_date",
    )

    search_fields = (
        "retailer__name",
        "transaction_id",
    )

    readonly_fields = ("payment_date",)

    autocomplete_fields = (
        "retailer",
        "subscription",
    )

    ordering = ("-payment_date",)
