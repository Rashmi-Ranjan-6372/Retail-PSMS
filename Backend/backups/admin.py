from django.contrib import admin
from .models import BackupLog


@admin.register(BackupLog)
class BackupLogAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "retailer",
        "backup_type",
        "status",
        "file_name",
        "file_size",
        "created_at",
    )

    list_filter = (
        "backup_type",
        "status",
        "created_at",
    )

    search_fields = (
        "file_name",
        "retailer__name",
    )

    ordering = (
        "-created_at",
    )