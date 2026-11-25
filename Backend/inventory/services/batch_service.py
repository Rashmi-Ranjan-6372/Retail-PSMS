from django.db import transaction
from django.utils import timezone

from inventory.models.stock_batch_models import StockBatch
from subscriptions.utils import (
    check_subscription_write_access,
    validate_branch_subscription,
)


class BatchService:

    @staticmethod
    def _validate_quantity(qty):

        try:
            qty = int(qty)
        except (TypeError, ValueError):
            raise ValueError("Quantity must be a valid integer.")

        if qty <= 0:
            raise ValueError("Quantity must be greater than 0.")

        return qty

    @staticmethod
    def _check_subscription(batch):

        check_subscription_write_access(batch.retailer)

        validate_branch_subscription(batch.retailer)

    # =====================================================
    # UPDATE AVAILABLE QUANTITY
    # =====================================================

    @staticmethod
    @transaction.atomic
    def update_available_qty(batch_id, qty, operation="minus"):

        try:
            batch = StockBatch.objects.select_for_update().get(id=batch_id)
        except StockBatch.DoesNotExist:
            raise ValueError("Stock batch not found.")

        BatchService._check_subscription(batch)

        qty = BatchService._validate_quantity(qty)

        if operation == "minus":

            if batch.available_qty < qty:
                raise ValueError(f"Insufficient stock in batch {batch.batch_no}.")

            batch.available_qty -= qty

        elif operation == "plus":

            if batch.available_qty + batch.reserved_qty + qty > batch.quantity:
                raise ValueError(
                    "Available quantity cannot exceed total stock "
                    "after considering reserved stock."
                )

            batch.available_qty += qty

        else:
            raise ValueError("Invalid operation. Use 'plus' or 'minus'.")

        batch.save(update_fields=["available_qty"])

        return batch

    # =====================================================
    # RESERVE STOCK
    # =====================================================

    @staticmethod
    @transaction.atomic
    def reserve_stock(batch_id, qty):

        try:
            batch = StockBatch.objects.select_for_update().get(id=batch_id)
        except StockBatch.DoesNotExist:
            raise ValueError("Stock batch not found.")

        BatchService._check_subscription(batch)

        qty = BatchService._validate_quantity(qty)

        if batch.available_qty < qty:
            raise ValueError(f"Not enough available stock in batch {batch.batch_no}.")

        batch.available_qty -= qty
        batch.reserved_qty += qty

        batch.save(update_fields=["available_qty", "reserved_qty"])

        return batch

    # =====================================================
    # RELEASE RESERVED STOCK
    # =====================================================

    @staticmethod
    @transaction.atomic
    def release_reserved_stock(batch_id, qty):

        try:
            batch = StockBatch.objects.select_for_update().get(id=batch_id)
        except StockBatch.DoesNotExist:
            raise ValueError("Stock batch not found.")

        BatchService._check_subscription(batch)

        qty = BatchService._validate_quantity(qty)

        if batch.reserved_qty < qty:
            raise ValueError(f"Reserved quantity exceeded in batch {batch.batch_no}.")

        batch.reserved_qty -= qty
        batch.available_qty += qty

        batch.save(update_fields=["available_qty", "reserved_qty"])

        return batch

    # =====================================================
    # GET AVAILABLE BATCHES
    # =====================================================

    @staticmethod
    def get_available_batches(product, branch):

        if not product:
            raise ValueError("Product is required.")

        if not branch:
            raise ValueError("Branch is required.")

        if product.retailer_id != branch.retailer_id:
            raise ValueError("Product and branch must belong to the same retailer.")

        return StockBatch.objects.filter(
            retailer_id=product.retailer_id,
            branch=branch,
            product=product,
            available_qty__gt=0,
            is_expired=False,
            expiry_date__gte=timezone.localdate(),
        ).order_by("expiry_date", "id")
