
from decimal import Decimal

from django.db import transaction
from django.db.models import Sum

from rest_framework import serializers

from inventory.models.sales_item_models import SalesItem
from inventory.models.stock_batch_models import StockBatch
from inventory.models.sales_models import Sales


class SalesItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesItem
        fields = "__all__"

        read_only_fields = [
            "retailer",
            "tax_amount",
            "amount",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        request = self.context.get("request")
        instance = self.instance

        sales = attrs.get(
            "sales",
            getattr(instance, "sales", None)
        )

        product = attrs.get(
            "product",
            getattr(instance, "product", None)
        )

        batch = attrs.get(
            "batch",
            getattr(instance, "batch", None)
        )

        branch = attrs.get(
            "branch",
            getattr(instance, "branch", None)
        )

        qty = attrs.get(
            "qty",
            getattr(instance, "qty", 0)
        )

        free_qty = attrs.get(
            "free_qty",
            getattr(instance, "free_qty", 0)
        )

        unit_price = attrs.get(
            "unit_price",
            getattr(instance, "unit_price", 0)
        )

        discount = attrs.get(
            "discount",
            getattr(instance, "discount", 0)
        )

        tax_percent = attrs.get(
            "tax_percent",
            getattr(instance, "tax_percent", 0)
        )

        if not sales:
            raise serializers.ValidationError({
                "sales": "Sales is required."
            })

        retailer = sales.retailer

        if request and request.user.is_authenticated:

            user_retailer = getattr(request.user, "retailer", None)

            if user_retailer and user_retailer.id != retailer.id:
                raise serializers.ValidationError({
                    "sales": "You cannot access another retailer's sales."
                })

            if not user_retailer and not request.user.is_superuser:
                raise serializers.ValidationError({
                    "sales": "Retailer account is required."
                })

        if sales.branch_id != (branch.id if branch else None):
            raise serializers.ValidationError({
                "branch": "Branch must match the selected sales record."
            })

        if product and product.retailer_id != retailer.id:
            raise serializers.ValidationError({
                "product": "Product does not belong to this retailer."
            })

        if batch:

            if batch.retailer_id != retailer.id:
                raise serializers.ValidationError({
                    "batch": "Batch does not belong to this retailer."
                })

            if product and batch.product_id != product.id:
                raise serializers.ValidationError({
                    "batch": "Batch does not belong to the selected product."
                })

            if batch.branch_id != (branch.id if branch else None):
                raise serializers.ValidationError({
                    "batch": "Batch does not belong to the selected branch."
                })

        if qty <= 0:
            raise serializers.ValidationError({
                "qty": "Quantity must be greater than 0."
            })

        if free_qty < 0:
            raise serializers.ValidationError({
                "free_qty": "Free quantity cannot be negative."
            })

        if unit_price < 0:
            raise serializers.ValidationError({
                "unit_price": "Unit price cannot be negative."
            })

        if discount < 0:
            raise serializers.ValidationError({
                "discount": "Discount cannot be negative."
            })

        if tax_percent < 0:
            raise serializers.ValidationError({
                "tax_percent": "Tax percentage cannot be negative."
            })

        base_amount = Decimal(str(qty)) * Decimal(str(unit_price))

        if discount > base_amount:
            raise serializers.ValidationError({
                "discount": "Discount cannot exceed the base amount."
            })

        attrs["retailer"] = retailer

        return attrs

    def calculate_amount(self, qty, unit_price, discount, tax_percent):

        qty = Decimal(str(qty))
        unit_price = Decimal(str(unit_price))
        discount = Decimal(str(discount))
        tax_percent = Decimal(str(tax_percent))

        base_amount = qty * unit_price

        discounted_amount = base_amount - discount

        tax_amount = (
            discounted_amount * tax_percent
        ) / Decimal("100")

        final_amount = discounted_amount + tax_amount

        return tax_amount, final_amount

    def update_sales_total(self, sales):

        total = (
            sales.items.aggregate(
                total=Sum("amount")
            )["total"] or Decimal("0.00")
        )

        sales.total_amount = total

        sales.save(update_fields=[
            "total_amount",
            "updated_at",
        ])

    def update_batch_stock(self, batch, quantity, restore=False):

        if restore:
            batch.available_qty += quantity
            batch.quantity += quantity

        else:
            if batch.available_qty < quantity:
                raise serializers.ValidationError({
                    "stock": (
                        f"Only {batch.available_qty} "
                        "items available in stock."
                    )
                })

            batch.available_qty -= quantity
            batch.quantity -= quantity

        batch.save(update_fields=[
            "available_qty",
            "quantity",
            "updated_at",
        ])

    @transaction.atomic
    def create(self, validated_data):

        sales = validated_data["sales"]

        batch = StockBatch.objects.select_for_update().get(
            id=validated_data["batch"].id
        )

        if batch.is_expired:
            raise serializers.ValidationError({
                "batch": "Cannot sell an expired batch."
            })

        from django.utils import timezone

        if (
            batch.expiry_date
            and batch.expiry_date < timezone.localdate()
        ):
            raise serializers.ValidationError({
                "batch": "Cannot sell an expired batch."
            })

        if batch.retailer_id != sales.retailer_id:
            raise serializers.ValidationError({
                "batch": "Batch does not belong to this retailer."
            })

        if batch.product_id != validated_data["product"].id:
            raise serializers.ValidationError({
                "batch": "Batch does not belong to this product."
            })

        if batch.branch_id != sales.branch_id:
            raise serializers.ValidationError({
                "batch": "Batch does not belong to this sales branch."
            })

        qty = validated_data.get("qty", 0)
        free_qty = validated_data.get("free_qty", 0)

        total_qty = qty + free_qty

        self.update_batch_stock(
            batch,
            total_qty
        )

        tax_amount, final_amount = self.calculate_amount(
            qty,
            validated_data.get("unit_price", 0),
            validated_data.get("discount", 0),
            validated_data.get("tax_percent", 0),
        )

        validated_data["batch"] = batch
        validated_data["retailer"] = sales.retailer
        validated_data["tax_amount"] = tax_amount
        validated_data["amount"] = final_amount

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        sales_item = SalesItem.objects.create(**validated_data)

        self.update_sales_total(sales)

        return sales_item

    @transaction.atomic
    def update(self, instance, validated_data):

        old_sales = instance.sales

        new_sales = validated_data.get(
            "sales",
            instance.sales
        )

        if new_sales.id != old_sales.id:
            raise serializers.ValidationError({
                "sales": "Moving an item to another sales record is not allowed."
            })

        old_batch_id = instance.batch_id

        new_batch_id = validated_data.get(
            "batch",
            instance.batch
        ).id

        batch_ids = sorted(set([old_batch_id, new_batch_id]))

        locked_batches = {
            batch.id: batch
            for batch in StockBatch.objects.select_for_update()
            .filter(id__in=batch_ids)
            .order_by("id")
        }

        old_batch = locked_batches.get(old_batch_id)
        new_batch = locked_batches.get(new_batch_id)

        if not old_batch or not new_batch:
            raise serializers.ValidationError({
                "batch": "Selected stock batch does not exist."
            })

        qty = validated_data.get("qty", instance.qty)
        free_qty = validated_data.get("free_qty", instance.free_qty)

        total_qty = qty + free_qty

        product = validated_data.get("product", instance.product)
        branch = validated_data.get("branch", instance.branch)

        if new_batch.retailer_id != old_sales.retailer_id:
            raise serializers.ValidationError({
                "batch": "Batch does not belong to this retailer."
            })

        if new_batch.product_id != product.id:
            raise serializers.ValidationError({
                "batch": "Batch does not belong to the selected product."
            })

        if new_batch.branch_id != (
            branch.id if branch else None
        ):
            raise serializers.ValidationError({
                "batch": "Batch does not belong to the selected branch."
            })

        from django.utils import timezone

        if (
            new_batch.is_expired
            or (
                new_batch.expiry_date
                and new_batch.expiry_date < timezone.localdate()
            )
        ):
            raise serializers.ValidationError({
                "batch": "Cannot sell an expired batch."
            })

        self.update_batch_stock(
            old_batch,
            instance.qty + instance.free_qty,
            restore=True
        )

        self.update_batch_stock(
            new_batch,
            total_qty
        )

        unit_price = validated_data.get(
            "unit_price",
            instance.unit_price
        )

        discount = validated_data.get(
            "discount",
            instance.discount
        )

        tax_percent = validated_data.get(
            "tax_percent",
            instance.tax_percent
        )

        tax_amount, final_amount = self.calculate_amount(
            qty,
            unit_price,
            discount,
            tax_percent,
        )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.batch = new_batch
        instance.retailer = old_sales.retailer
        instance.tax_amount = tax_amount
        instance.amount = final_amount

        instance.save()

        self.update_sales_total(old_sales)

        return instance

    @transaction.atomic
    def delete(self, instance):

        sales = instance.sales

        batch = StockBatch.objects.select_for_update().get(
            id=instance.batch_id
        )

        total_qty = instance.qty + instance.free_qty

        self.update_batch_stock(
            batch,
            total_qty,
            restore=True
        )

        instance.delete()

        self.update_sales_total(sales)
