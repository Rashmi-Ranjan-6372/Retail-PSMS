from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import (
    ExpenseCategory,
    Expense,
    ExpenseAttachment,
)


# ==========================================================
#                    HELPER FUNCTIONS
# ==========================================================
def get_user_scope(user):
    if user.is_superuser or getattr(user, "role", None) == "platform_owner":
        return "platform"

    return "retailer"


def validate_retailer_category(category, retailer_id):
    if category.scope != "retailer":
        raise serializers.ValidationError(
            "Retailer expenses must use a retailer expense category."
        )

    if category.retailer_id != retailer_id:
        raise serializers.ValidationError(
            "Selected category does not belong to your retailer."
        )


# ==========================================================
#                 EXPENSE CATEGORY SERIALIZER
# ==========================================================
class ExpenseCategorySerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(
        source="retailer.name",
        read_only=True,
    )

    created_by_name = serializers.CharField(
        source="created_by.get_full_name",
        read_only=True,
    )

    class Meta:
        model = ExpenseCategory
        fields = (
            "id",
            "scope",
            "retailer",
            "retailer_name",
            "name",
            "description",
            "is_active",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "scope",
            "retailer",
            "created_by",
            "created_at",
            "updated_at",
        )

    def validate_name(self, value):
        return value.strip()

    def validate(self, attrs):
        user = self.context["request"].user

        if get_user_scope(user) == "platform":
            attrs["scope"] = "platform"
            attrs["retailer"] = None
        else:
            if not user.retailer_id:
                raise serializers.ValidationError(
                    "You are not associated with any retailer."
                )

            attrs["scope"] = "retailer"
            attrs["retailer"] = user.retailer

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user

        instance = ExpenseCategory(**validated_data)

        try:
            instance.full_clean()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict)

        instance.save()
        return instance


# ==========================================================
#                    EXPENSE SERIALIZER
# ==========================================================
class ExpenseSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(
        source="retailer.name",
        read_only=True,
    )

    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True,
    )

    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    created_by_name = serializers.CharField(
        source="created_by.get_full_name",
        read_only=True,
    )

    total_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Expense
        fields = (
            "id",
            "scope",
            "retailer",
            "retailer_name",
            "branch",
            "branch_name",
            "category",
            "category_name",
            "expense_number",
            "title",
            "description",
            "expense_date",
            "amount",
            "tax_amount",
            "total_amount",
            "payment_method",
            "payment_reference",
            "vendor_name",
            "invoice_number",
            "status",
            "notes",
            "created_by",
            "created_by_name",
            "approved_by",
            "approved_at",
            "paid_at",
            "cancelled_by",
            "cancelled_at",
            "cancellation_reason",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "scope",
            "retailer",
            "branch",
            "expense_number",
            "status",
            "created_by",
            "approved_by",
            "approved_at",
            "paid_at",
            "cancelled_by",
            "cancelled_at",
            "cancellation_reason",
            "created_at",
            "updated_at",
            "total_amount",
        )

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Expense amount must be greater than zero."
            )
        return value

    def validate_tax_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Tax amount cannot be negative.")
        return value

    def validate_category(self, category):
        user = self.context["request"].user

        if get_user_scope(user) == "platform":
            if category.scope != "platform" or category.retailer_id is not None:
                raise serializers.ValidationError(
                    "Platform expenses must use a platform expense category."
                )
        else:
            if not user.retailer_id:
                raise serializers.ValidationError(
                    "You are not associated with any retailer."
                )

            validate_retailer_category(category, user.retailer_id)

        if not category.is_active:
            raise serializers.ValidationError("Selected expense category is inactive.")

        return category

    def validate(self, attrs):
        user = self.context["request"].user
        category = attrs.get(
            "category",
            getattr(self.instance, "category", None),
        )

        if get_user_scope(user) == "platform":
            attrs["scope"] = "platform"
            attrs["retailer"] = None
            attrs["branch"] = None

            if category and category.scope != "platform":
                raise serializers.ValidationError(
                    {"category": "Select a platform expense category."}
                )

            return attrs

        if not user.retailer_id:
            raise serializers.ValidationError(
                "You are not associated with any retailer."
            )

        attrs["scope"] = "retailer"
        attrs["retailer"] = user.retailer

        branch = attrs.get(
            "branch",
            getattr(self.instance, "branch", None),
        )

        if getattr(user, "role", None) == "superadmin":
            if branch is not None:
                if (
                    branch.retailer_id != user.retailer_id
                    or not branch.is_active
                    or branch.deleted_at is not None
                ):
                    raise serializers.ValidationError(
                        {
                            "branch": "Select a valid active branch belonging to your retailer."
                        }
                    )
        else:
            user_branch = getattr(user, "branch", None)

            if (
                user_branch is None
                or not user_branch.is_active
                or user_branch.deleted_at is not None
            ):
                raise serializers.ValidationError(
                    "You are not assigned to an active branch."
                )

            attrs["branch"] = user_branch

        if category:
            validate_retailer_category(category, user.retailer_id)

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user

        instance = Expense(**validated_data)

        try:
            instance.full_clean()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict)

        instance.save()
        return instance

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        try:
            instance.full_clean()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict)

        instance.save()
        return instance


# ==========================================================
#                EXPENSE ATTACHMENT SERIALIZER
# ==========================================================
class ExpenseAttachmentSerializer(serializers.ModelSerializer):

    uploaded_by_name = serializers.CharField(
        source="uploaded_by.get_full_name",
        read_only=True,
    )

    class Meta:
        model = ExpenseAttachment
        fields = (
            "id",
            "expense",
            "file",
            "file_name",
            "uploaded_by",
            "uploaded_by_name",
            "uploaded_at",
        )

        read_only_fields = (
            "id",
            "uploaded_by",
            "uploaded_at",
        )

    def validate_expense(self, expense):
        user = self.context["request"].user

        if get_user_scope(user) == "platform":
            if expense.scope != "platform":
                raise serializers.ValidationError(
                    "You cannot attach files to retailer expenses."
                )
        else:
            if expense.scope != "retailer" or expense.retailer_id != user.retailer_id:
                raise serializers.ValidationError(
                    "You cannot attach files to another retailer's expense."
                )

            if getattr(user, "role", None) != "superadmin":
                if expense.branch_id != getattr(user, "branch_id", None):
                    raise serializers.ValidationError(
                        "You cannot attach files to another branch's expense."
                    )

        return expense

    def create(self, validated_data):
        validated_data["uploaded_by"] = self.context["request"].user
        return super().create(validated_data)
