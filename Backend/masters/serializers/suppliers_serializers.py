from rest_framework import serializers

from masters.models.suppliers_models import Supplier
from branches.models import Branch


class SupplierSerializer(serializers.ModelSerializer):

    branches = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Branch.objects.all(), required=False
    )

    retailer_name = serializers.CharField(source="retailer.name", read_only=True)

    branch_names = serializers.SerializerMethodField()

    class Meta:
        model = Supplier

        fields = [
            "id",
            "retailer",
            "retailer_name",
            "branches",
            "branch_names",
            "name",
            "contact_person",
            "phone",
            "alternate_phone",
            "email",
            "gst_no",
            "drug_license_no",
            "address",
            "city",
            "state",
            "pincode",
            "opening_balance",
            "is_active",
            "deleted_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "retailer",
            "retailer_name",
            "branch_names",
            "is_active",
            "deleted_at",
            "created_at",
            "updated_at",
        )

    def get_branch_names(self, obj):
        return [branch.name for branch in obj.branches.all()]

    def get_retailer(self):
        retailer = self.context.get("retailer")

        if not retailer:
            raise serializers.ValidationError({"retailer": "Retailer is required."})

        return retailer

    def validate_name(self, value):
        value = value.strip().title()

        if not value:
            raise serializers.ValidationError("Supplier name is required.")

        return value

    def validate_phone(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Phone number is required.")

        return value

    def validate_gst_no(self, value):
        value = (value or "").strip().upper()

        return value or None

    def validate(self, data):
        request = self.context.get("request")

        if not request:
            raise serializers.ValidationError("Request context is required.")

        user = request.user
        retailer = self.get_retailer()

        is_platform_owner = user.is_superuser
        user_branch = getattr(user, "branch", None)

        if self.instance:
            if self.instance.retailer_id != retailer.id:
                raise serializers.ValidationError("You cannot modify this supplier.")

        branches = data.get("branches")

        # ================= BRANCH VALIDATION =================

        if branches is not None:

            if not branches:
                raise serializers.ValidationError(
                    {"branches": "At least one branch is required."}
                )

            for branch in branches:
                if branch.retailer_id != retailer.id:
                    raise serializers.ValidationError(
                        {
                            "branches": "Selected branch does not belong to this retailer."
                        }
                    )

            # Branch admins cannot modify branch assignments
            if not is_platform_owner and user_branch:

                if self.instance:
                    raise serializers.ValidationError(
                        {
                            "branches": "Branch admins cannot change supplier branch assignments."
                        }
                    )

                if any(branch.id != user_branch.id for branch in branches):
                    raise serializers.ValidationError(
                        {
                            "branches": "You can assign suppliers only to your own branch."
                        }
                    )

        # ================= CREATE BRANCH VALIDATION =================

        if not self.instance:

            if not is_platform_owner and user_branch:

                if branches is not None:
                    if any(branch.id != user_branch.id for branch in branches):
                        raise serializers.ValidationError(
                            {
                                "branches": "You can assign suppliers only to your own branch."
                            }
                        )

            elif branches is None:
                raise serializers.ValidationError(
                    {"branches": "At least one branch must be selected."}
                )

        # ================= DUPLICATE VALIDATION =================

        name = data.get("name", self.instance.name if self.instance else None)

        phone = data.get("phone", self.instance.phone if self.instance else None)

        gst_no = data.get("gst_no", self.instance.gst_no if self.instance else None)

        queryset = Supplier.objects.filter(retailer=retailer)

        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if name and queryset.filter(name__iexact=name).exists():
            raise serializers.ValidationError({"name": "Supplier name already exists."})

        if phone and queryset.filter(phone=phone).exists():
            raise serializers.ValidationError({"phone": "Phone number already exists."})

        if gst_no and queryset.filter(gst_no__iexact=gst_no).exists():
            raise serializers.ValidationError({"gst_no": "GST number already exists."})

        return data

    def create(self, validated_data):
        user = self.context["request"].user

        retailer = self.get_retailer()
        branches = validated_data.pop("branches", None)

        supplier = Supplier.objects.create(retailer=retailer, **validated_data)

        if user.is_superuser:
            supplier.branches.set(branches)

        elif getattr(user, "branch", None):
            supplier.branches.set([user.branch])

        else:
            supplier.branches.set(branches)

        return supplier

    def update(self, instance, validated_data):
        user = self.context["request"].user

        branches = validated_data.pop("branches", None)

        validated_data.pop("retailer", None)

        supplier = super().update(instance, validated_data)

        if not user.is_superuser and not getattr(user, "branch", None):
            if branches is not None:
                supplier.branches.set(branches)

        elif user.is_superuser:
            if branches is not None:
                supplier.branches.set(branches)

        return supplier
