from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction

from inventory.models.sales_models import Sales
from inventory.models.sales_return_models import SalesReturn
from inventory.models.sales_return_item_models import SalesReturnItem
from inventory.models.stock_batch_models import StockBatch


@transaction.atomic
def process_sales_return(sales_return_id):

    # Lock sales return.
    try:
        sales_return = (
            SalesReturn.objects
            .select_for_update()
            .select_related("retailer", "branch")
            .get(pk=sales_return_id)
        )
    except SalesReturn.DoesNotExist:
        raise ValueError("Sales return not found.")

    if sales_return.status == "COMPLETED":
        raise ValueError("Sales return has already been processed.")

    if sales_return.status != "DRAFT":
        raise ValueError("Only draft sales returns can be processed.")

    # Lock original sale.
    try:
        sales = Sales.objects.select_for_update().get(
            pk=sales_return.sales_id
        )
    except Sales.DoesNotExist:
        raise ValueError("Original sales invoice not found.")

    if sales.retailer_id != sales_return.retailer_id:
        raise ValueError(
            "Sales invoice does not belong to this retailer."
        )

    if sales.branch_id != sales_return.branch_id:
        raise ValueError(
            "Sales return branch does not match the original sales branch."
        )

    if sales.status == "CANCELLED":
        raise ValueError("Cannot process a return for cancelled sales.")

    # Lock return items.
    items = list(
        SalesReturnItem.objects
        .select_for_update()
        .filter(sales_return=sales_return)
        .order_by("id")
    )

    if not items:
        raise ValueError(
            "Cannot process a sales return without return items."
        )

    total_return_amount = Decimal("0.00")

    for item in items:

        if item.retailer_id != sales_return.retailer_id:
            raise ValueError(
                "Return item does not belong to this retailer."
            )

        if item.branch_id != sales_return.branch_id:
            raise ValueError(
                "Return item branch does not match the sales return branch."
            )

        qty = Decimal(str(item.qty or 0))
        free_qty = Decimal(str(item.free_qty or 0))

        if qty < 0 or free_qty < 0:
            raise ValueError("Return quantities cannot be negative.")

        return_qty = qty + free_qty

        if return_qty <= 0:
            raise ValueError(
                f"Return quantity must be greater than zero for item {item.id}."
            )

        try:
            batch = StockBatch.objects.select_for_update().get(
                pk=item.batch_id
            )
        except StockBatch.DoesNotExist:
            raise ValueError(
                f"Stock batch not found for return item {item.id}."
            )

        if batch.retailer_id != item.retailer_id:
            raise ValueError(
                "Stock batch does not belong to this retailer."
            )

        if batch.branch_id != item.branch_id:
            raise ValueError(
                "Stock batch does not belong to this branch."
            )

        if batch.product_id != item.product_id:
            raise ValueError(
                "Stock batch does not belong to the selected product."
            )

        if item.return_condition == "RESELLABLE":

            batch.quantity += return_qty
            batch.available_qty += return_qty

            try:
                batch.save(
                    update_fields=[
                        "quantity",
                        "available_qty",
                        "updated_at",
                    ]
                )
            except DjangoValidationError as exc:
                raise ValueError(str(exc))

        try:
            item_amount = Decimal(str(item.amount or 0))
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError(
                f"Invalid return amount for item {item.id}."
            )

        if item_amount < 0:
            raise ValueError(
                f"Return amount cannot be negative for item {item.id}."
            )

        total_return_amount += item_amount

    sales_return.total_amount = total_return_amount

    sales_return.status = "COMPLETED"

    try:
        sales_return.save(
            update_fields=[
                "total_amount",
                "status",
                "updated_at",
            ]
        )
    except DjangoValidationError as exc:
        raise ValueError(str(exc))

    return sales_return