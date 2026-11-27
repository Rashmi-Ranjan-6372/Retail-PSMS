from rest_framework import serializers

from .models import (
    SupportCategory,
    SupportTicket,
    SupportMessage,
    SupportAttachment,
    PlatformSupportInfo,
    TicketActivity,
)

# ==========================================================
# SUPPORT CATEGORY SERIALIZER
# ==========================================================


class SupportCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportCategory

        fields = [
            "id",
            "name",
            "description",
            "is_active",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError("Category name cannot be empty.")

        queryset = SupportCategory.objects.filter(name__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "A category with this name already exists."
            )

        return value


# ==========================================================
# SUPPORT ATTACHMENT SERIALIZER
# ==========================================================


class SupportAttachmentSerializer(serializers.ModelSerializer):

    uploaded_by_name = serializers.CharField(
        source="uploaded_by.username", read_only=True, allow_null=True
    )

    class Meta:
        model = SupportAttachment

        fields = [
            "id",
            "ticket",
            "uploaded_by",
            "uploaded_by_name",
            "file",
            "uploaded_at",
        ]

        read_only_fields = [
            "id",
            "ticket",
            "uploaded_by",
            "uploaded_at",
        ]


class CreateSupportAttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportAttachment

        fields = [
            "file",
        ]


# ==========================================================
# SUPPORT MESSAGE SERIALIZER
# ==========================================================


class SupportMessageSerializer(serializers.ModelSerializer):

    sender_name = serializers.CharField(
        source="sender.username", read_only=True, allow_null=True
    )

    class Meta:
        model = SupportMessage

        fields = [
            "id",
            "ticket",
            "sender",
            "sender_name",
            "message",
            "is_platform_reply",
            "is_read",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "ticket",
            "sender",
            "sender_name",
            "is_platform_reply",
            "is_read",
            "created_at",
        ]


class ReplySupportTicketSerializer(serializers.Serializer):

    message = serializers.CharField(
        required=True, allow_blank=False, trim_whitespace=True
    )

    attachment = serializers.FileField(required=False, allow_null=True)

    def validate_message(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError("Reply message cannot be empty.")

        return value


# ==========================================================
# TICKET ACTIVITY SERIALIZER
# ==========================================================


class TicketActivitySerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(
        source="user.username", read_only=True, allow_null=True
    )

    class Meta:
        model = TicketActivity

        fields = [
            "id",
            "ticket",
            "user",
            "user_name",
            "action",
            "remarks",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "ticket",
            "user",
            "user_name",
            "action",
            "remarks",
            "created_at",
        ]


# ==========================================================
# SUPPORT TICKET SERIALIZER
# ==========================================================


class SupportTicketSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(source="retailer.name", read_only=True)

    branch_name = serializers.CharField(
        source="branch.name", read_only=True, allow_null=True
    )

    created_by_name = serializers.CharField(
        source="created_by.username", read_only=True, allow_null=True
    )

    assigned_to_name = serializers.CharField(
        source="assigned_to.username", read_only=True, allow_null=True
    )

    category_name = serializers.CharField(
        source="category.name", read_only=True, allow_null=True
    )

    attachments = SupportAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = SupportTicket

        fields = [
            "id",
            "ticket_number",
            "retailer",
            "retailer_name",
            "branch",
            "branch_name",
            "created_by",
            "created_by_name",
            "category",
            "category_name",
            "subject",
            "description",
            "priority",
            "status",
            "assigned_to",
            "assigned_to_name",
            "is_private",
            "resolved_at",
            "created_at",
            "updated_at",
            "attachments",
        ]

        read_only_fields = fields


# ==========================================================
# SUPPORT TICKET LIST SERIALIZER
# ==========================================================


class SupportTicketListSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(source="retailer.name", read_only=True)

    branch_name = serializers.CharField(
        source="branch.name", read_only=True, allow_null=True
    )

    created_by_name = serializers.CharField(
        source="created_by.username", read_only=True, allow_null=True
    )

    assigned_to_name = serializers.CharField(
        source="assigned_to.username", read_only=True, allow_null=True
    )

    category_name = serializers.CharField(
        source="category.name", read_only=True, allow_null=True
    )

    class Meta:
        model = SupportTicket

        fields = [
            "id",
            "ticket_number",
            "subject",
            "retailer_name",
            "branch_name",
            "created_by_name",
            "category_name",
            "assigned_to_name",
            "priority",
            "status",
            "created_at",
        ]

        read_only_fields = fields


# ==========================================================
# SUPPORT TICKET DETAIL SERIALIZER
# ==========================================================


class SupportTicketDetailSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(source="retailer.name", read_only=True)

    branch_name = serializers.CharField(
        source="branch.name", read_only=True, allow_null=True
    )

    created_by_name = serializers.CharField(
        source="created_by.username", read_only=True, allow_null=True
    )

    assigned_to_name = serializers.CharField(
        source="assigned_to.username", read_only=True, allow_null=True
    )

    category_name = serializers.CharField(
        source="category.name", read_only=True, allow_null=True
    )

    messages = SupportMessageSerializer(many=True, read_only=True)

    attachments = SupportAttachmentSerializer(many=True, read_only=True)

    activities = TicketActivitySerializer(many=True, read_only=True)

    class Meta:
        model = SupportTicket

        fields = [
            "id",
            "ticket_number",
            "retailer",
            "retailer_name",
            "branch",
            "branch_name",
            "created_by",
            "created_by_name",
            "category",
            "category_name",
            "subject",
            "description",
            "priority",
            "status",
            "assigned_to",
            "assigned_to_name",
            "is_private",
            "resolved_at",
            "created_at",
            "updated_at",
            "messages",
            "attachments",
            "activities",
        ]

        read_only_fields = fields


# ==========================================================
# CREATE SUPPORT TICKET SERIALIZER
# ==========================================================


class CreateSupportTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportTicket

        fields = [
            "category",
            "subject",
            "description",
            "priority",
        ]

    def validate_category(self, value):

        if value and not value.is_active:
            raise serializers.ValidationError("This support category is inactive.")

        return value

    def validate_subject(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError("Ticket subject cannot be empty.")

        return value

    def validate_description(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError("Ticket description cannot be empty.")

        return value


# ==========================================================
# UPDATE TICKET STATUS SERIALIZER
# ==========================================================


class UpdateTicketStatusSerializer(serializers.Serializer):

    status = serializers.ChoiceField(
        choices=SupportTicket.STATUS_CHOICES, required=True
    )

    remarks = serializers.CharField(required=False, allow_blank=True, allow_null=True)


# ==========================================================
# ASSIGN SUPPORT TICKET SERIALIZER
# ==========================================================


class AssignTicketSerializer(serializers.Serializer):

    assigned_to = serializers.IntegerField(required=True, min_value=1, allow_null=True)

    remarks = serializers.CharField(required=False, allow_blank=True, allow_null=True)


# ==========================================================
# PLATFORM SUPPORT INFORMATION SERIALIZER
# ==========================================================


class PlatformSupportInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlatformSupportInfo

        fields = [
            "id",
            "company_name",
            "support_email",
            "support_mobile",
            "whatsapp_number",
            "website",
            "address",
            "support_hours",
            "is_active",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "updated_at",
        ]

    def validate_company_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError("Company name cannot be empty.")

        return value
