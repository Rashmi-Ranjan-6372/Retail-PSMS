from django.db import transaction

from inventory.models.expiry_damage_models import (
    ExpiryDamage
)

from inventory.models.stock_batch_models import (
    StockBatch
)


# =====================================================
# CREATE EXPIRY / DAMAGE ENTRY
# =====================================================

def create_expiry_damage(data, user):

    with transaction.atomic():

        batch = data["batch"]

        quantity = data["quantity"]

        # =========================
        # VALIDATE STOCK
        # =========================

        if batch.available_qty < quantity:

            raise ValueError(
                "Insufficient stock available."
            )

        # =========================
        # CREATE ENTRY
        # =========================

        expiry_damage = ExpiryDamage.objects.create(
            retailer=user.retailer,
            branch=user.branch,
            created_by=user,
            **data
        )

        # =========================
        # REDUCE STOCK
        # =========================

        batch.available_qty -= quantity

        batch.save()

        return expiry_damage


# =====================================================
# UPDATE EXPIRY / DAMAGE ENTRY
# =====================================================

def update_expiry_damage(instance, validated_data):

    with transaction.atomic():

        old_qty = instance.quantity

        old_batch = instance.batch

        new_qty = validated_data.get(
            "quantity",
            instance.quantity
        )

        new_batch = validated_data.get(
            "batch",
            instance.batch
        )

        # =========================
        # RESTORE OLD STOCK
        # =========================

        old_batch.available_qty += old_qty
        old_batch.save()

        # =========================
        # VALIDATE NEW STOCK
        # =========================

        if new_batch.available_qty < new_qty:

            raise ValueError(
                "Insufficient stock available."
            )

        # =========================
        # DEDUCT NEW STOCK
        # =========================

        new_batch.available_qty -= new_qty
        new_batch.save()

        # =========================
        # UPDATE INSTANCE
        # =========================

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        return instance


# =====================================================
# DELETE EXPIRY / DAMAGE ENTRY
# =====================================================

def delete_expiry_damage(instance):

    with transaction.atomic():

        batch = instance.batch

        batch.available_qty += instance.quantity

        batch.save()

        instance.delete()