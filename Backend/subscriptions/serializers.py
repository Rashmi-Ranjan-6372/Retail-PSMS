from rest_framework import serializers

from .models import (
    SubscriptionPlan,
    RetailerSubscription,
    PaymentHistory
)

from accounts.models import Retailer


# =====================================================
# SUBSCRIPTION PLAN
# =====================================================

class SubscriptionPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionPlan

        fields = "__all__"

        read_only_fields = (
            "id",
            "created_at",
            "updated_at"
        )


# =====================================================
# RETAILER SUBSCRIPTION
# =====================================================

class RetailerSubscriptionSerializer(
    serializers.ModelSerializer
):

    retailer_name = serializers.CharField(
        source="retailer.name",
        read_only=True
    )

    plan_name = serializers.CharField(
        source="plan.name",
        read_only=True
    )

    class Meta:
        model = RetailerSubscription

        fields = [
            "id",
            "retailer",
            "retailer_name",
            "plan",
            "plan_name",
            "start_date",
            "expiry_date",
            "status",
            "auto_renew",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at"
        )


# =====================================================
# CREATE / UPDATE RETAILER SUBSCRIPTION
# =====================================================

class RetailerSubscriptionCreateSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = RetailerSubscription

        fields = [
            "retailer",
            "plan",
            "start_date",
            "expiry_date",
            "status",
            "auto_renew",
        ]

    def validate(self, attrs):

        retailer = attrs.get("retailer")

        if RetailerSubscription.objects.filter(
            retailer=retailer
        ).exists():

            raise serializers.ValidationError(
                "Retailer already has a subscription."
            )

        return attrs


# =====================================================
# PAYMENT HISTORY
# =====================================================

class PaymentHistorySerializer(
    serializers.ModelSerializer
):

    retailer_name = serializers.CharField(
        source="retailer.name",
        read_only=True
    )

    plan_name = serializers.CharField(
        source="subscription.plan.name",
        read_only=True
    )

    class Meta:
        model = PaymentHistory

        fields = [
            "id",
            "retailer",
            "retailer_name",
            "subscription",
            "plan_name",
            "amount",
            "payment_status",
            "transaction_id",
            "payment_date",
        ]

        read_only_fields = (
            "id",
            "payment_date"
        )


# =====================================================
# CREATE PAYMENT
# =====================================================

class PaymentHistoryCreateSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = PaymentHistory

        fields = [
            "retailer",
            "subscription",
            "amount",
            "payment_status",
            "transaction_id",
        ]