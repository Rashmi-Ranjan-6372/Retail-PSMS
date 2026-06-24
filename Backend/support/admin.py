from django.contrib import admin
from .models import (
    SupportCategory,
    SupportTicket,
    SupportMessage,
    SupportAttachment,
    PlatformSupportInfo,
    TicketActivity,
)


@admin.register(SupportCategory)
class SupportCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):

    list_display = (
        "ticket_number",
        "subject",
        "retailer",
        "branch",
        "created_by",
        "priority",
        "status",
        "assigned_to",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
        "retailer",
        "branch",
        "created_at",
    )

    search_fields = (
        "ticket_number",
        "subject",
        "retailer__name",
        "created_by__username",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "ticket_number",
        "created_at",
        "updated_at",
        "resolved_at",
    )


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "ticket",
        "sender",
        "is_platform_reply",
        "is_read",
        "created_at",
    )

    list_filter = (
        "is_platform_reply",
        "is_read",
        "created_at",
    )

    search_fields = (
        "ticket__ticket_number",
        "sender__username",
        "message",
    )

    ordering = (
        "-created_at",
    )


@admin.register(SupportAttachment)
class SupportAttachmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "ticket",
        "uploaded_by",
        "file",
        "uploaded_at",
    )

    list_filter = (
        "uploaded_at",
    )

    search_fields = (
        "ticket__ticket_number",
        "uploaded_by__username",
    )

    ordering = (
        "-uploaded_at",
    )


@admin.register(PlatformSupportInfo)
class PlatformSupportInfoAdmin(admin.ModelAdmin):

    list_display = (
        "company_name",
        "support_email",
        "support_mobile",
        "whatsapp_number",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "company_name",
        "support_email",
        "support_mobile",
    )

    ordering = (
        "-updated_at",
    )


@admin.register(TicketActivity)
class TicketActivityAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "ticket",
        "user",
        "action",
        "created_at",
    )

    list_filter = (
        "action",
        "created_at",
    )

    search_fields = (
        "ticket__ticket_number",
        "user__username",
        "action",
    )

    ordering = (
        "-created_at",
    )