from decimal import Decimal
from django.db import transaction
from inventory.models.sales_models import Sales
from inventory.models.sales_item_models import SalesItem
from inventory.models.stock_batch_models import StockBatch
from inventory.utils.expiry_checker import is_batch_expired
from subscriptions.utils import check_subscription_write_access, validate_branch_subscription
from accounts.views import create_audit_log

@transaction.atomic
def create_sale(
            *,
            retailer,
            branch,
            customer,
            items,
            paid_amount,
            created_by,
            discount=0,
            remarks=None,
            request=None
        ):
    if not created_by.is_superuser:
        check_subscription_write_access(retailer)
        validate_branch_subscription(branch)

    total_amount=Decimal("0.00")
    paid_amount=Decimal(str(paid_amount or 0))
    discount=Decimal(str(discount or 0))

    sale=Sales.objects.create(
        retailer=retailer,
        branch=branch,
        customer=customer,
        paid_amount=paid_amount,
        discount=discount,
        remarks=remarks,
        created_by=created_by,
    )

    for item in items:
        batch=StockBatch.objects.select_for_update().get(
            id=item["batch"],
            retailer=retailer
        )

        qty=int(item.get("qty",0))
        free_qty=int(item.get("free_qty",0))
        item_discount=Decimal(str(item.get("discount",0)))
        tax_percent=Decimal(str(item.get("tax_percent",0)))

        if batch.branch!=branch:
            raise ValueError(
                f"{batch.product.name} does not belong to this branch"
            )

        if batch.is_expired or is_batch_expired(batch):
            raise ValueError(
                f"{batch.product.name} batch is expired"
            )

        total_required_qty=qty+free_qty

        if batch.available_qty<total_required_qty:
            raise ValueError(
                f"Insufficient stock for {batch.product.name}"
            )

        batch.available_qty-=total_required_qty
        batch.save(update_fields=["available_qty"])

        unit_price=batch.sale_price

        base_amount=Decimal(str(qty))*Decimal(str(unit_price))
        discounted_amount=base_amount-item_discount
        tax_amount=(discounted_amount*tax_percent)/Decimal("100")
        final_amount=discounted_amount+tax_amount

        total_amount+=final_amount

        SalesItem.objects.create(
            retailer=retailer,
            branch=branch,
            sales=sale,
            product=batch.product,
            batch=batch,
            qty=qty,
            free_qty=free_qty,
            unit_price=unit_price,
            discount=item_discount,
            tax_percent=tax_percent,
            tax_amount=tax_amount,
            amount=final_amount,
            created_by=created_by,
        )

    sale.total_amount=total_amount
    sale.save()

    if request:
        create_audit_log(
            user=created_by,
            action="create",
            model_name="Sales",
            object_id=sale.id,
            description=f"Created Sale {sale.id} Amount:{sale.total_amount}",
            request=request
        )

    return sale


def update_sales_totals(
    sale,
    request=None
):
    items=sale.items.all()

    total_amount=Decimal("0.00")

    for item in items:
        total_amount+=(
            item.amount or Decimal("0.00")
        )

    old_amount=sale.total_amount

    sale.total_amount=total_amount

    sale.save(
        update_fields=[
            "total_amount",
            "net_amount",
            "due_amount",
            "payment_status",
        ]
    )

    if request:
        create_audit_log(
            user=request.user,
            action="update",
            model_name="Sales",
            object_id=sale.id,
            description=f"Updated Sale Totals from {old_amount} to {sale.total_amount}",
            request=request
        )

    return sale