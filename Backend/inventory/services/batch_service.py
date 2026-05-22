from django.db import transaction
from django.db.models import F

from inventory.models.stock_batch_models import (
    StockBatch
)


class BatchService:

    # =====================================================
    # UPDATE AVAILABLE QUANTITY
    # =====================================================

    @staticmethod
    @transaction.atomic
    def update_available_qty(
        batch_id,
        qty,
        operation="minus"
    ):

        batch = (
            StockBatch.objects
            .select_for_update()
            .get(id=batch_id)
        )

        qty = int(qty)

        # =========================
        # MINUS STOCK
        # =========================

        if operation == "minus":

            if batch.available_qty < qty:

                raise ValueError(
                    f"Insufficient stock in batch "
                    f"{batch.batch_no}"
                )

            batch.available_qty = (
                batch.available_qty - qty
            )

        # =========================
        # ADD STOCK
        # =========================

        elif operation == "plus":

            batch.available_qty = (
                batch.available_qty + qty
            )

        else:

            raise ValueError(
                "Invalid operation. "
                "Use 'plus' or 'minus'."
            )

        batch.save(
            update_fields=["available_qty"]
        )

        return batch

    # =====================================================
    # RESERVE STOCK
    # =====================================================

    @staticmethod
    @transaction.atomic
    def reserve_stock(
        batch_id,
        qty
    ):

        batch = (
            StockBatch.objects
            .select_for_update()
            .get(id=batch_id)
        )

        qty = int(qty)

        if batch.available_qty < qty:

            raise ValueError(
                "Not enough available stock."
            )

        batch.available_qty -= qty

        batch.reserved_qty += qty

        batch.save(
            update_fields=[
                "available_qty",
                "reserved_qty"
            ]
        )

        return batch

    # =====================================================
    # RELEASE RESERVED STOCK
    # =====================================================

    @staticmethod
    @transaction.atomic
    def release_reserved_stock(
        batch_id,
        qty
    ):

        batch = (
            StockBatch.objects
            .select_for_update()
            .get(id=batch_id)
        )

        qty = int(qty)

        if batch.reserved_qty < qty:

            raise ValueError(
                "Reserved quantity exceeded."
            )

        batch.reserved_qty -= qty

        batch.available_qty += qty

        batch.save(
            update_fields=[
                "available_qty",
                "reserved_qty"
            ]
        )

        return batch

    # =====================================================
    # GET AVAILABLE BATCHES
    # =====================================================

    @staticmethod
    def get_available_batches(
        product
    ):

        return (
            StockBatch.objects.filter(
                product=product,
                available_qty__gt=0,
                is_expired=False
            )
            .order_by("expiry_date")
        )