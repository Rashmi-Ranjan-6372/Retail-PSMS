from rest_framework import serializers

from masters.models.suppliers_models import Supplier
from branches.models import Branch


class SupplierSerializer(serializers.ModelSerializer):

    branches = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Branch.objects.all(),
        required=False
    )

    retailer_name = serializers.CharField(
        source="retailer.name",
        read_only=True
    )

    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True
    )

    branch_names = serializers.SerializerMethodField()

    class Meta:
        model = Supplier

        fields = [
            "id",

            # ================= RETAILER =================
            "retailer",
            "retailer_name",

            # ================= PRIMARY BRANCH =================
            "branch",
            "branch_name",

            # ================= MULTI BRANCH =================
            "branches",
            "branch_names",

            # ================= BASIC =================
            "name",
            "contact_person",

            # ================= CONTACT =================
            "phone",
            "alternate_phone",
            "email",

            # ================= LEGAL =================
            "gst_no",
            "drug_license_no",

            # ================= ADDRESS =================
            "address",
            "city",
            "state",
            "pincode",

            # ================= FINANCE =================
            "opening_balance",

            # ================= STATUS =================
            "is_active",
            "deleted_at",

            # ================= TIMESTAMPS =================
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "retailer",
            "branch",
            "retailer_name",
            "branch_name",
            "branch_names",
            "created_at",
            "updated_at",
        )

    def get_branch_names(self, obj):

        return [
            branch.name
            for branch in obj.branches.all()
        ]

    def validate(self, data):

        request = self.context["request"]
        user = request.user

        branches = data.get("branches", [])

        # ================= SUPERUSER =================

        if user.is_superuser:

            if not branches:
                raise serializers.ValidationError({
                    "branches":
                    "This field is required for superuser."
                })

            invalid_branch = branches.exclude(
                retailer=user.retailer
            ).exists()

            if invalid_branch:
                raise serializers.ValidationError({
                    "branches":
                    "Invalid retailer branches selected."
                })

        # ================= NORMAL ADMIN =================

        else:
            data.pop("branches", None)

        return data

    def validate_name(self, value):

        value = value.strip().title()

        request = self.context["request"]
        user = request.user

        queryset = Supplier.objects.filter(
            retailer=user.retailer,
            name__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(
                id=self.instance.id
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "Supplier name already exists"
            )

        return value

    def validate_phone(self, value):

        request = self.context["request"]
        user = request.user

        queryset = Supplier.objects.filter(
            retailer=user.retailer,
            phone=value
        )

        if self.instance:
            queryset = queryset.exclude(
                id=self.instance.id
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "Phone number already exists"
            )

        return value

    def validate_gst_no(self, value):

        if value:

            request = self.context["request"]
            user = request.user

            queryset = Supplier.objects.filter(
                retailer=user.retailer,
                gst_no__iexact=value
            )

            if self.instance:
                queryset = queryset.exclude(
                    id=self.instance.id
                )

            if queryset.exists():
                raise serializers.ValidationError(
                    "GST number already exists"
                )

        return value

    def create(self, validated_data):

        request = self.context["request"]
        user = request.user

        branches = validated_data.pop("branches", [])

        validated_data["retailer"] = user.retailer
        validated_data["branch"] = user.branch

        supplier = Supplier.objects.create(
            **validated_data
        )

        # ================= SUPERUSER =================

        if user.is_superuser:
            supplier.branches.set(branches)

        # ================= NORMAL ADMIN =================

        else:
            supplier.branches.set([user.branch])

        return supplier

    def update(self, instance, validated_data):

        request = self.context["request"]
        user = request.user

        branches = validated_data.pop("branches", None)

        validated_data.pop("retailer", None)
        validated_data.pop("branch", None)

        supplier = super().update(
            instance,
            validated_data
        )

        # ================= SUPERUSER =================

        if user.is_superuser and branches is not None:
            supplier.branches.set(branches)

        # ================= NORMAL ADMIN =================

        elif not user.is_superuser:
            supplier.branches.set([user.branch])

        return supplier