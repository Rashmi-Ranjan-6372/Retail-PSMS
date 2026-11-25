
from rest_framework import serializers

from django.utils import timezone

from inventory.models.stock_batch_models import StockBatch


class StockBatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockBatch
        fields = "__all__"

        read_only_fields = [
            "retailer",
            "is_expired",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        request = self.context.get("request")
        instance = self.instance

        retailer = (
            attrs.get("retailer")
            or getattr(instance, "retailer", None)
        )

        branch = attrs.get(
            "branch",
            getattr(instance, "branch", None)
        )

        product = attrs.get(
            "product",
            getattr(instance, "product", None)
        )

        supplier = attrs.get(
            "supplier",
            getattr(instance, "supplier", None)
        )

        quantity = attrs.get(
            "quantity",
            getattr(instance, "quantity", 0)
        )

        available_qty = attrs.get(
            "available_qty",
            getattr(instance, "available_qty", 0)
        )

        reserved_qty = attrs.get(
            "reserved_qty",
            getattr(instance, "reserved_qty", 0)
        )

        purchase_price = attrs.get(
            "purchase_price",
            getattr(instance, "purchase_price", 0)
        )

        sale_price = attrs.get(
            "sale_price",
            getattr(instance, "sale_price", 0)
        )

        mrp = attrs.get(
            "mrp",
            getattr(instance, "mrp", 0)
        )

        expiry_date = attrs.get(
            "expiry_date",
            getattr(instance, "expiry_date", None)
        )

        manufacture_date = attrs.get(
            "manufacture_date",
            getattr(instance, "manufacture_date", None)
        )

        if request and request.user.is_authenticated:

            user_retailer = getattr(
                request.user,
                "retailer",
                None
            )

            if user_retailer:
                retailer = user_retailer

            elif not request.user.is_superuser:
                raise serializers.ValidationError({
                    "retailer": "Retailer account is required."
                })

        if not retailer:
            raise serializers.ValidationError({
                "retailer": "Retailer is required."
            })

        if not branch:
            raise serializers.ValidationError({
                "branch": "Branch is required."
            })

        if branch.retailer_id != retailer.id:
            raise serializers.ValidationError({
                "branch": "Branch does not belong to this retailer."
            })

        if product and product.retailer_id != retailer.id:
            raise serializers.ValidationError({
                "product": "Product does not belong to this retailer."
            })

        if supplier and supplier.retailer_id != retailer.id:
            raise serializers.ValidationError({
                "supplier": "Supplier does not belong to this retailer."
            })

        if quantity < 0:
            raise serializers.ValidationError({
                "quantity": "Quantity cannot be negative."
            })

        if available_qty < 0:
            raise serializers.ValidationError({
                "available_qty": "Available quantity cannot be negative."
            })

        if reserved_qty < 0:
            raise serializers.ValidationError({
                "reserved_qty": "Reserved quantity cannot be negative."
            })

        if available_qty + reserved_qty > quantity:
            raise serializers.ValidationError({
                "available_qty": (
                    "Available quantity and reserved quantity "
                    "cannot exceed total quantity."
                )
            })

        if purchase_price < 0:
            raise serializers.ValidationError({
                "purchase_price": "Purchase price cannot be negative."
            })

        if sale_price < 0:
            raise serializers.ValidationError({
                "sale_price": "Sale price cannot be negative."
            })

        if mrp < 0:
            raise serializers.ValidationError({
                "mrp": "MRP cannot be negative."
            })

        if sale_price > mrp:
            raise serializers.ValidationError({
                "sale_price": "Sale price cannot exceed MRP."
            })

        if (
            manufacture_date
            and expiry_date
            and manufacture_date > expiry_date
        ):
            raise serializers.ValidationError({
                "expiry_date": (
                    "Expiry date cannot be earlier than manufacture date."
                )
            })

        if expiry_date and expiry_date < timezone.localdate():
            raise serializers.ValidationError({
                "expiry_date": "Cannot create or update an already expired batch."
            })

        attrs["retailer"] = retailer

        return attrs

    def create(self, validated_data):

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        return super().create(validated_data)
