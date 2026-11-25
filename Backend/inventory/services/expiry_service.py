
from django.db import transaction

from inventory.models.expiry_damage_models import ExpiryDamage
from inventory.models.stock_batch_models import StockBatch

from subscriptions.utils import (
    check_subscription_write_access,
    validate_branch_subscription
)


# =====================================================
# COMMON VALIDATION
# =====================================================

def validate_quantity(quantity):

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        raise ValueError("Quantity must be a valid integer.")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")

    return quantity


def check_stock_subscription(retailer):

    check_subscription_write_access(retailer)
    validate_branch_subscription(retailer)


def lock_batches(batch_ids):

    batches = (
        StockBatch.objects
        .select_for_update()
        .filter(id__in=batch_ids)
        .order_by("id")
    )

    batch_map = {
        batch.id: batch
        for batch in batches
    }

    if len(batch_map) != len(set(batch_ids)):
        raise ValueError("One or more stock batches were not found.")

    return batch_map


def validate_batch_ownership(batch, retailer, branch):

    if batch.retailer_id != retailer.id:
        raise ValueError(
            "Batch does not belong to this retailer."
        )

    if not branch or batch.branch_id != branch.id:
        raise ValueError(
            "Batch does not belong to this branch."
        )


def validate_stock_restoration(batch, quantity):

    if (
        batch.available_qty
        + batch.reserved_qty
        + quantity
        > batch.quantity
    ):
        raise ValueError(
            f"Cannot restore stock in batch {batch.batch_no}. "
            "Available and reserved quantities would exceed total stock."
        )


# =====================================================
# CREATE EXPIRY / DAMAGE ENTRY
# =====================================================

@transaction.atomic
def create_expiry_damage(data, user):

    retailer = getattr(user, "retailer", None)
    branch = getattr(user, "branch", None)

    if not retailer:
        raise ValueError("Retailer account is required.")

    if not branch:
        raise ValueError("Branch is required.")

    check_stock_subscription(retailer)

    data = data.copy()

    batch = data.pop("batch", None)
    quantity = validate_quantity(data.pop("quantity", None))

    if not batch:
        raise ValueError("Stock batch is required.")

    batch_map = lock_batches([batch.id])
    batch = batch_map[batch.id]

    validate_batch_ownership(
        batch,
        retailer,
        branch
    )

    if batch.available_qty < quantity:
        raise ValueError(
            f"Insufficient available stock in batch {batch.batch_no}."
        )

    # Do not accept tenant or user details from client data.
    data.pop("retailer", None)
    data.pop("branch", None)
    data.pop("created_by", None)

    expiry_damage = ExpiryDamage.objects.create(
        retailer=retailer,
        branch=branch,
        batch=batch,
        quantity=quantity,
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

@transaction.atomic
def update_expiry_damage(instance, validated_data):

    retailer = instance.retailer

    check_stock_subscription(retailer)

    # Lock the expiry/damage entry first.
    try:
        instance = (
            ExpiryDamage.objects
            .select_for_update()
            .get(id=instance.id)
        )
    except ExpiryDamage.DoesNotExist:
        raise ValueError("Expiry/damage entry not found.")

    validated_data = validated_data.copy()

    new_batch = validated_data.pop(
        "batch",
        instance.batch
    )

    new_quantity = validate_quantity(
        validated_data.pop(
            "quantity",
            instance.quantity
        )
    )

    # Tenant, branch and creator cannot be changed here.
    validated_data.pop("retailer", None)
    validated_data.pop("branch", None)
    validated_data.pop("created_by", None)

    old_batch_id = instance.batch_id
    new_batch_id = new_batch.id

    # Lock both batches in a consistent order.
    batch_map = lock_batches(
        list(set([old_batch_id, new_batch_id]))
    )

    old_batch = batch_map[old_batch_id]
    new_batch = batch_map[new_batch_id]

    validate_batch_ownership(
        old_batch,
        retailer,
        instance.branch
    )

    validate_batch_ownership(
        new_batch,
        retailer,
        instance.branch
    )

    old_quantity = instance.quantity

    # Restore the old entry quantity temporarily.
    restored_old_available = (
        old_batch.available_qty + old_quantity
    )

    if (
        restored_old_available + old_batch.reserved_qty
        > old_batch.quantity
    ):
        raise ValueError(
            "Cannot restore the previous expiry/damage quantity. "
            "Batch stock is inconsistent."
        )

    if old_batch_id == new_batch_id:

        available_after_restore = restored_old_available

        if available_after_restore < new_quantity:
            raise ValueError(
                f"Insufficient available stock in batch "
                f"{new_batch.batch_no}."
            )

        old_batch.available_qty = (
            available_after_restore - new_quantity
        )

        old_batch.save(
            update_fields=["available_qty"]
        )

    else:

        if new_batch.available_qty < new_quantity:
            raise ValueError(
                f"Insufficient available stock in batch "
                f"{new_batch.batch_no}."
            )

        old_batch.available_qty = restored_old_available
        new_batch.available_qty -= new_quantity

        old_batch.save(
            update_fields=["available_qty"]
        )

        new_batch.save(
            update_fields=["available_qty"]
        )

    # Update the expiry/damage entry.
    instance.batch = new_batch
    instance.quantity = new_quantity

    for attr, value in validated_data.items():
        setattr(instance, attr, value)

    instance.save()

    return instance


# =====================================================
# DELETE EXPIRY / DAMAGE ENTRY
# =====================================================

@transaction.atomic
def delete_expiry_damage(instance):

    retailer = instance.retailer

    check_stock_subscription(retailer)

    try:
        instance = (
            ExpiryDamage.objects
            .select_for_update()
            .get(id=instance.id)
        )
    except ExpiryDamage.DoesNotExist:
        raise ValueError("Expiry/damage entry not found.")

    batch_map = lock_batches([instance.batch_id])
    batch = batch_map[instance.batch_id]

    validate_batch_ownership(
        batch,
        retailer,
        instance.branch
    )

    validate_stock_restoration(
        batch,
        instance.quantity
    )

    batch.available_qty += instance.quantity

    batch.save(
        update_fields=["available_qty"]
    )

    instance.delete()

    return True
