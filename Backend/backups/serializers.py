from rest_framework import serializers

from .models import (
    BackupLog,
    BackupSchedule,
)

# ============================================================
# BACKUP LOG SERIALIZER
# ============================================================


class BackupLogSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(
        source="retailer.name", read_only=True, allow_null=True
    )

    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True, allow_null=True
    )

    restored_by_username = serializers.CharField(
        source="restored_by.username", read_only=True, allow_null=True
    )

    file_size_mb = serializers.SerializerMethodField()

    class Meta:
        model = BackupLog

        fields = [
            "id",
            "retailer",
            "retailer_name",
            "backup_type",
            "backup_scope",
            "status",
            "file_name",
            "file_size",
            "file_size_mb",
            "checksum",
            "download_count",
            "notes",
            "created_by",
            "created_by_username",
            "restored_by",
            "restored_by_username",
            "created_at",
            "updated_at",
            "restored_at",
        ]

        read_only_fields = [
            "id",
            "retailer",
            "retailer_name",
            "backup_type",
            "backup_scope",
            "status",
            "file_name",
            "file_size",
            "file_size_mb",
            "checksum",
            "download_count",
            "notes",
            "created_by",
            "created_by_username",
            "restored_by",
            "restored_by_username",
            "created_at",
            "updated_at",
            "restored_at",
        ]

    def get_file_size_mb(self, obj):
        return round(obj.file_size / (1024 * 1024), 2)


# ============================================================
# MANUAL BACKUP SERIALIZER
# ============================================================


class ManualBackupSerializer(serializers.Serializer):

    backup_scope = serializers.ChoiceField(
        choices=BackupLog.BackupScope.choices, default=BackupLog.BackupScope.DATABASE
    )

    notes = serializers.CharField(required=False, allow_blank=True, allow_null=False)


# ============================================================
# RESTORE BACKUP SERIALIZER
# ============================================================


class RestoreBackupSerializer(serializers.Serializer):

    backup_id = serializers.IntegerField(min_value=1)

    def validate_backup_id(self, value):

        try:
            backup = BackupLog.objects.get(id=value, retailer__isnull=True)
        except BackupLog.DoesNotExist:
            raise serializers.ValidationError("Platform backup does not exist.")

        if backup.status not in [
            BackupLog.Status.SUCCESS,
            BackupLog.Status.RESTORED,
        ]:
            raise serializers.ValidationError(
                "Only successful backups can be restored."
            )

        if not backup.file_path:
            raise serializers.ValidationError("Backup file path is missing.")

        if not backup.checksum:
            raise serializers.ValidationError(
                "Backup checksum is missing. Restoration is not allowed."
            )

        return value


# ============================================================
# BACKUP HISTORY SERIALIZER
# ============================================================


class BackupHistorySerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(
        source="retailer.name", read_only=True, allow_null=True
    )

    class Meta:
        model = BackupLog

        fields = [
            "id",
            "retailer_name",
            "backup_type",
            "backup_scope",
            "status",
            "file_name",
            "file_size",
            "created_at",
            "updated_at",
            "restored_at",
        ]

        read_only_fields = fields


# ============================================================
# BACKUP SCHEDULE SERIALIZER
# ============================================================


class BackupScheduleSerializer(serializers.ModelSerializer):

    updated_by_username = serializers.CharField(
        source="updated_by.username",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = BackupSchedule

        fields = [
            "id",
            "frequency",
            "backup_scope",
            "backup_time",
            "is_active",
            "last_run_at",
            "updated_by",
            "updated_by_username",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "last_run_at",
            "updated_by",
            "updated_by_username",
            "created_at",
            "updated_at",
        ]

    def validate_backup_time(self, value):
        if value is None:
            raise serializers.ValidationError("Backup time is required.")
        return value
