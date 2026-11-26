from django.contrib import admin

from .models import BackupLog, BackupSchedule


@admin.register(BackupLog)
class BackupLogAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "backup_type",
        "backup_scope",
        "status",
        "file_name",
        "file_size",
        "download_count",
        "created_by",
        "restored_by",
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
        "created_by__username",
        "restored_by__username",
    )

    readonly_fields = (
        "file_name",
        "file_path",
        "file_size",
        "checksum",
        "download_count",
        "created_at",
        "updated_at",
        "restored_at",
        "created_by",
        "restored_by",
    )

    ordering = ("-created_at",)
    list_per_page = 25
    date_hierarchy = "created_at"


@admin.register(BackupSchedule)
class BackupScheduleAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "frequency",
        "backup_scope",
        "backup_time",
        "is_active",
        "last_run_at",
        "updated_by",
        "updated_at",
    )

    list_filter = (
        "frequency",
        "backup_scope",
        "is_active",
    )

    readonly_fields = (
        "last_run_at",
        "updated_by",
        "created_at",
        "updated_at",
    )

    list_per_page = 25
