from django.db import transaction
from inventory.models.expiry_damage_models import ExpiryDamage
from inventory.models.stock_batch_models import StockBatch
from subscriptions.utils import (check_subscription_write_access, validate_branch_subscription)


# =====================================================
# CREATE EXPIRY / DAMAGE ENTRY
# =====================================================

def create_expiry_damage(data, user):

    check_subscription_write_access(user.retailer)
    validate_branch_subscription(user.retailer)

    with transaction.atomic():

        batch = data["batch"]
        quantity = data["quantity"]

        if batch.available_qty < quantity:

            raise ValueError(
                "Insufficient stock available."
            )

        expiry_damage = ExpiryDamage.objects.create(
            retailer=user.retailer,
            branch=user.branch,
            created_by=user,
            **data
        )

        batch.available_qty -= quantity

        batch.save(
            update_fields=["available_qty"]
        )

        return expiry_damage


# =====================================================
# UPDATE EXPIRY / DAMAGE ENTRY
# =====================================================

def update_expiry_damage(instance, validated_data):

    check_subscription_write_access(instance.retailer)
    validate_branch_subscription(instance.retailer)

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

        old_batch.available_qty += old_qty

        old_batch.save(
            update_fields=["available_qty"]
        )

        if new_batch.available_qty < new_qty:

            raise ValueError(
                "Insufficient stock available."
            )

        new_batch.available_qty -= new_qty

        new_batch.save(
            update_fields=["available_qty"]
        )

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        return instance


# =====================================================
# DELETE EXPIRY / DAMAGE ENTRY
# =====================================================

def delete_expiry_damage(instance):

    check_subscription_write_access(instance.retailer)
    validate_branch_subscription(instance.retailer)

    with transaction.atomic():

        batch = instance.batch
        batch.available_qty += instance.quantity
        batch.save(
            update_fields=["available_qty"]
        )

        instance.delete()