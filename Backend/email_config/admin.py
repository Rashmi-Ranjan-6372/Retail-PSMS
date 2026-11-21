
from django.contrib import admin

from .models import (
    PlatformEmailConfiguration,
    RetailerEmailConfiguration
)


@admin.register(PlatformEmailConfiguration)
class PlatformEmailConfigurationAdmin(admin.ModelAdmin):

    list_display = (
        "email_host_user",
        "smtp_host",
        "smtp_port",
        "is_verified",
        "is_active",
        "last_tested_at",
    )

    readonly_fields = (
        "encrypted_email_host_password",
        "created_at",
        "updated_at",
        "last_tested_at",
    )


@admin.register(RetailerEmailConfiguration)
class RetailerEmailConfigurationAdmin(admin.ModelAdmin):

    list_display = (
        "retailer",
        "email_host_user",
        "smtp_host",
        "smtp_port",
        "is_verified",
        "is_active",
    )

    search_fields = (
        "retailer__name",
        "email_host_user",
        "smtp_host",
    )

    readonly_fields = (
        "encrypted_email_host_password",
        "created_at",
        "updated_at",
        "last_tested_at",
    )
