from django.contrib import admin
from .models import (
    BackupLog,
    BackupSchedule
)


@admin.register(BackupLog)
class BackupLogAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "retailer",
        "backup_type",
        "backup_scope",
        "status",
        "file_name",
        "file_size",
        "download_count",
        "created_by",
        "created_at",
    )

    list_filter = (
        "backup_type",
        "backup_scope",
        "status",
        "created_at",
    )

    search_fields = (
        "file_name",
        "retailer__name",
        "created_by__username",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "restored_at",
    )


@admin.register(BackupSchedule)
class BackupScheduleAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "retailer",
        "frequency",
        "backup_time",
        "is_active",
        "created_at",
    )

    list_filter = (
        "frequency",
        "is_active",
        "created_at",
    )

    search_fields = (
        "retailer__name",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )