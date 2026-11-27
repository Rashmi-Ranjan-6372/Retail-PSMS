from decimal import Decimal

from django.utils import timezone

from rest_framework import serializers

from .models import (
    SubscriptionPlan,
    RetailerSubscription,
    PaymentHistory,
)

from accounts.models import Retailer

# ==========================================================
# SUBSCRIPTION PLAN SERIALIZER
# ==========================================================


class SubscriptionPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionPlan

        fields = [
            "id",
            "name",
            "plan_type",
            "monthly_price",
            "yearly_price",
            "max_users",
            "max_branches",
            "max_products",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_monthly_price(self, value):

        if value < Decimal("0.00"):
            raise serializers.ValidationError("Monthly price cannot be negative.")

        return value

    def validate_yearly_price(self, value):

        if value < Decimal("0.00"):
            raise serializers.ValidationError("Yearly price cannot be negative.")

        return value


# ==========================================================
# RETAILER SUBSCRIPTION SERIALIZER
# ==========================================================


class RetailerSubscriptionSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(source="retailer.name", read_only=True)
    plan_name = serializers.CharField(source="plan.name", read_only=True)
    plan_type = serializers.CharField(source="plan.plan_type", read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_active = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = RetailerSubscription

        fields = [
            "id",
            "retailer",
            "retailer_name",
            "plan",
            "plan_name",
            "plan_type",
            "billing_cycle",
            "amount",
            "start_date",
            "expiry_date",
            "status",
            "is_active",
            "is_expired",
            "auto_renew",
            "cancelled_at",
            "cancelled_reason",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "retailer_name",
            "plan_name",
            "plan_type",
            "amount",
            "is_active",
            "is_expired",
            "created_at",
            "updated_at",
        ]

    def get_is_active(self, obj):

        return obj.is_active()

    def get_is_expired(self, obj):

        return obj.is_expired()


# ==========================================================
# CREATE RETAILER SUBSCRIPTION SERIALIZER
# ==========================================================


class RetailerSubscriptionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RetailerSubscription

        fields = [
            "retailer",
            "plan",
            "billing_cycle",
            "start_date",
            "expiry_date",
            "status",
            "auto_renew",
        ]

    def validate_retailer(self, value):

        if RetailerSubscription.objects.filter(retailer=value).exists():

            raise serializers.ValidationError(
                "This retailer already has a subscription."
            )

        return value

    def validate_plan(self, value):

        if not value.is_active:

            raise serializers.ValidationError("This subscription plan is inactive.")

        return value

    def validate(self, attrs):

        start_date = attrs.get("start_date")
        expiry_date = attrs.get("expiry_date")

        if start_date and expiry_date:

            if start_date >= expiry_date:

                raise serializers.ValidationError(
                    {"expiry_date": ("Expiry date must be later than start date.")}
                )

        return attrs

    def create(self, validated_data):

        return RetailerSubscription.objects.create(**validated_data)


# ==========================================================
# UPDATE RETAILER SUBSCRIPTION SERIALIZER
# ==========================================================


class RetailerSubscriptionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RetailerSubscription

        fields = [
            "plan",
            "billing_cycle",
            "start_date",
            "expiry_date",
            "status",
            "auto_renew",
            "cancelled_at",
            "cancelled_reason",
        ]

    def validate_plan(self, value):

        if not value.is_active:

            raise serializers.ValidationError(
                "You cannot assign an inactive subscription plan."
            )

        return value

    def validate(self, attrs):

        instance = self.instance

        start_date = attrs.get("start_date", instance.start_date if instance else None)

        expiry_date = attrs.get(
            "expiry_date", instance.expiry_date if instance else None
        )

        if start_date and expiry_date:

            if start_date >= expiry_date:

                raise serializers.ValidationError(
                    {"expiry_date": ("Expiry date must be later than start date.")}
                )

        return attrs


# ==========================================================
# PAYMENT HISTORY SERIALIZER
# ==========================================================


class PaymentHistorySerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(source="retailer.name", read_only=True)
    plan_name = serializers.CharField(source="subscription.plan.name", read_only=True)

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

        read_only_fields = [
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


# ==========================================================
# CREATE PAYMENT HISTORY SERIALIZER
# ==========================================================


class PaymentHistoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentHistory

        fields = [
            "retailer",
            "subscription",
            "amount",
            "transaction_id",
        ]

    def validate_amount(self, value):

        if value <= Decimal("0.00"):

            raise serializers.ValidationError(
                "Payment amount must be greater than zero."
            )

        return value

    def validate_transaction_id(self, value):

        if value:

            value = value.strip()

            if not value:
                return None

            if PaymentHistory.objects.filter(transaction_id=value).exists():

                raise serializers.ValidationError("This transaction ID already exists.")

        return value

    def validate(self, attrs):

        retailer = attrs.get("retailer")
        subscription = attrs.get("subscription")

        if retailer and subscription:

            if subscription.retailer_id != retailer.id:

                raise serializers.ValidationError(
                    {
                        "subscription": (
                            "The selected subscription does not belong "
                            "to the selected retailer."
                        )
                    }
                )

        return attrs

    def create(self, validated_data):

        validated_data["payment_status"] = "pending"

        return PaymentHistory.objects.create(**validated_data)
