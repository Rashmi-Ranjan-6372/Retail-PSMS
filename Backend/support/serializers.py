from rest_framework import serializers

from .models import (
    SupportCategory,
    SupportTicket,
    SupportMessage,
    SupportAttachment,
    PlatformSupportInfo,
    TicketActivity,
)


class SupportCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportCategory
        fields = "__all__"


class SupportAttachmentSerializer(serializers.ModelSerializer):

    uploaded_by_name = serializers.CharField(
        source="uploaded_by.username",
        read_only=True
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
            "uploaded_by",
            "uploaded_at",
        ]


class SupportMessageSerializer(serializers.ModelSerializer):

    sender_name = serializers.CharField(
        source="sender.username",
        read_only=True
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
            "sender",
            "is_platform_reply",
            "created_at",
        ]


class TicketActivitySerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(
        source="user.username",
        read_only=True
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


class SupportTicketSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(source="retailer.name",read_only=True)
    branch_name = serializers.CharField(source="branch.name",read_only=True)
    created_by_name = serializers.CharField(source="created_by.username",read_only=True)
    assigned_to_name = serializers.CharField(source="assigned_to.username",read_only=True)
    category_name = serializers.CharField(source="category.name",read_only=True)
    attachments = SupportAttachmentSerializer(many=True,read_only=True)

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

        read_only_fields = [
            "ticket_number",
            "retailer",
            "branch",
            "created_by",
            "resolved_at",
            "created_at",
            "updated_at",
        ]


class SupportTicketListSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(source="retailer.name",read_only=True)
    branch_name = serializers.CharField(source="branch.name",read_only=True)
    created_by_name = serializers.CharField(source="created_by.username",read_only=True)

    class Meta:
        model = SupportTicket
        fields = [
            "id",
            "ticket_number",
            "subject",
            "retailer_name",
            "branch_name",
            "created_by_name",
            "priority",
            "status",
            "created_at",
        ]


class SupportTicketDetailSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(source="retailer.name",read_only=True)
    branch_name = serializers.CharField(source="branch.name",read_only=True)
    created_by_name = serializers.CharField(source="created_by.username",read_only=True)
    assigned_to_name = serializers.CharField(source="assigned_to.username",read_only=True)
    category_name = serializers.CharField(source="category.name",read_only=True)
    messages = SupportMessageSerializer(many=True,read_only=True)
    attachments = SupportAttachmentSerializer(many=True,read_only=True)
    activities = TicketActivitySerializer(many=True,read_only=True)

    class Meta:
        model = SupportTicket
        fields = [
            "id",
            "ticket_number",
            "retailer_name",
            "branch_name",
            "created_by_name",
            "category_name",
            "subject",
            "description",
            "priority",
            "status",
            "assigned_to_name",
            "is_private",
            "resolved_at",
            "created_at",
            "updated_at",
            "messages",
            "attachments",
            "activities",
        ]


class CreateSupportTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportTicket
        fields = [
            "category",
            "subject",
            "description",
            "priority",
        ]


class ReplySupportTicketSerializer(serializers.Serializer):

    message = serializers.CharField()


class UpdateTicketStatusSerializer(serializers.Serializer):

    status = serializers.ChoiceField(
        choices=SupportTicket.STATUS_CHOICES
    )


class AssignTicketSerializer(serializers.Serializer):

    assigned_to = serializers.IntegerField()


class PlatformSupportInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlatformSupportInfo
        fields = "__all__"