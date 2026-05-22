# =====================================================
# SALES ITEM BUSINESS LOGIC
# =====================================================

from decimal import Decimal
from django.db import transaction
from inventory import models
from rest_framework import serializers

from inventory.models.sales_item_models import SalesItem
from inventory.models.stock_batch_models import StockBatch
from inventory.models.sales_models import Sales


class SalesItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesItem
        fields = "__all__"

        read_only_fields = [
            "tax_amount",
            "amount",
            "created_by",
            "created_at",
            "updated_at",
        ]

    # =====================================================
    # CREATE SALES ITEM
    # =====================================================

    @transaction.atomic
    def create(self, validated_data):

        batch = validated_data["batch"]

        qty = validated_data.get("qty", 0)
        free_qty = validated_data.get("free_qty", 0)

        total_qty = qty + free_qty

        # =================================================
        # STOCK VALIDATION
        # =================================================

        if batch.available_qty < total_qty:

            raise serializers.ValidationError({
                "stock": (
                    f"Only {batch.available_qty} "
                    f"items available in stock."
                )
            })

        # =================================================
        # CALCULATE BASE AMOUNT
        # =================================================

        unit_price = Decimal(
            validated_data.get("unit_price", 0)
        )

        discount = Decimal(
            validated_data.get("discount", 0)
        )

        tax_percent = Decimal(
            validated_data.get("tax_percent", 0)
        )

        base_amount = (
            Decimal(qty) * unit_price
        )

        discounted_amount = (
            base_amount - discount
        )

        tax_amount = (
            discounted_amount * tax_percent
        ) / Decimal("100")

        final_amount = (
            discounted_amount + tax_amount
        )

        validated_data["tax_amount"] = tax_amount
        validated_data["amount"] = final_amount

        # =================================================
        # CREATE SALES ITEM
        # =================================================

        sales_item = SalesItem.objects.create(
            **validated_data
        )

        # =================================================
        # UPDATE STOCK
        # =================================================

        batch.available_qty -= total_qty
        batch.save()

        # =================================================
        # UPDATE SALES TOTAL
        # =================================================

        sales = sales_item.sales

        total = (
            sales.items.aggregate(
                total=models.Sum("amount")
            )["total"] or 0
        )

        sales.total_amount = total
        sales.save()

        return sales_item

    # =====================================================
    # UPDATE SALES ITEM
    # =====================================================

    @transaction.atomic
    def update(self, instance, validated_data):

        old_total_qty = (
            instance.qty +
            instance.free_qty
        )

        old_batch = instance.batch

        # =================================================
        # RETURN OLD STOCK
        # =================================================

        old_batch.available_qty += old_total_qty
        old_batch.save()

        # =================================================
        # NEW VALUES
        # =================================================

        new_batch = validated_data.get(
            "batch",
            instance.batch
        )

        qty = validated_data.get(
            "qty",
            instance.qty
        )

        free_qty = validated_data.get(
            "free_qty",
            instance.free_qty
        )

        total_qty = qty + free_qty

        # =================================================
        # STOCK VALIDATION
        # =================================================

        if new_batch.available_qty < total_qty:

            raise serializers.ValidationError({
                "stock": (
                    f"Only {new_batch.available_qty} "
                    f"items available in stock."
                )
            })

        # =================================================
        # UPDATE STOCK
        # =================================================

        new_batch.available_qty -= total_qty
        new_batch.save()

        # =================================================
        # UPDATE FIELDS
        # =================================================

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # =================================================
        # RECALCULATE
        # =================================================

        base_amount = (
            Decimal(instance.qty) *
            Decimal(instance.unit_price)
        )

        discounted_amount = (
            base_amount -
            Decimal(instance.discount)
        )

        instance.tax_amount = (
            discounted_amount *
            Decimal(instance.tax_percent)
        ) / Decimal("100")

        instance.amount = (
            discounted_amount +
            instance.tax_amount
        )

        instance.save()

        # =================================================
        # UPDATE SALES TOTAL
        # =================================================

        sales = instance.sales

        total = (
            sales.items.aggregate(
                total=models.Sum("amount")
            )["total"] or 0
        )

        sales.total_amount = total
        sales.save()

        return instance

    # =====================================================
    # DELETE SALES ITEM
    # =====================================================

    @transaction.atomic
    def delete(self, instance):

        batch = instance.batch

        total_qty = (
            instance.qty +
            instance.free_qty
        )

        # =================================================
        # RETURN STOCK
        # =================================================

        batch.available_qty += total_qty
        batch.save()

        sales = instance.sales

        instance.delete()

        # =================================================
        # UPDATE SALES TOTAL
        # =================================================

        total = (
            sales.items.aggregate(
                total=models.Sum("amount")
            )["total"] or 0
        )

        sales.total_amount = total
        sales.save()