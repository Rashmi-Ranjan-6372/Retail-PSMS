from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(
        source="retailer.name",
        read_only=True,
        allow_null=True,
    )

    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True,
        allow_null=True,
    )

    recipient_name = serializers.CharField(
        source="recipient.get_full_name",
        read_only=True,
    )

    recipient_email = serializers.EmailField(
        source="recipient.email",
        read_only=True,
    )

    notification_type_display = serializers.CharField(
        source="get_notification_type_display",
        read_only=True,
    )

    priority_display = serializers.CharField(
        source="get_priority_display",
        read_only=True,
    )

    scope_display = serializers.CharField(
        source="get_scope_display",
        read_only=True,
    )

    class Meta:
        model = Notification

        fields = [
            "id",
            "scope",
            "scope_display",
            "retailer",
            "retailer_name",
            "branch",
            "branch_name",
            "recipient",
            "recipient_name",
            "recipient_email",
            "title",
            "message",
            "notification_type",
            "notification_type_display",
            "priority",
            "priority_display",
            "is_read",
            "read_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "scope",
            "retailer",
            "branch",
            "recipient",
            "title",
            "message",
            "notification_type",
            "priority",
            "is_read",
            "read_at",
            "created_at",
            "updated_at",
        ]
