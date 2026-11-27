from django.contrib import admin

from notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "scope",
        "notification_type",
        "priority",
        "retailer",
        "branch",
        "recipient",
        "is_read",
        "created_at",
    )

    list_display_links = (
        "id",
        "title",
    )

    list_filter = (
        "scope",
        "notification_type",
        "priority",
        "is_read",
        "created_at",
    )

    search_fields = (
        "title",
        "message",
        "recipient__email",
        "recipient__username",
        "retailer__name",
        "branch__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "read_at",
    )

    ordering = ("-created_at",)

    list_per_page = 25

    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Notification Information",
            {
                "fields": (
                    "scope",
                    "notification_type",
                    "priority",
                    "title",
                    "message",
                )
            },
        ),
        (
            "Recipient Information",
            {
                "fields": (
                    "recipient",
                    "retailer",
                    "branch",
                )
            },
        ),
        (
            "Read Status",
            {
                "fields": (
                    "is_read",
                    "read_at",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.select_related(
            "recipient",
            "retailer",
            "branch",
        )
