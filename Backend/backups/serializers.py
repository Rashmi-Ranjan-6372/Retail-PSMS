from rest_framework import serializers

from .models import BackupLog, BackupSchedule

# ============================================================
#                      BACKUP LOG SERIALIZER
# ============================================================


class BackupLogSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(source="retailer.name", read_only=True)

    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )

    restored_by_username = serializers.CharField(
        source="restored_by.username", read_only=True
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
            "file_path",
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
            "restored_at",
        ]

        read_only_fields = [
            "id",
            "file_size_mb",
            "download_count",
            "created_by",
            "created_by_username",
            "restored_by",
            "restored_by_username",
            "created_at",
            "restored_at",
        ]

    def get_file_size_mb(self, obj):
        return round(obj.file_size / (1024 * 1024), 2)

    def validate_file_size(self, value):

        if value < 0:
            raise serializers.ValidationError("File size cannot be negative.")

        return value


# ============================================================
#                    MANUAL BACKUP SERIALIZER
# ============================================================


class ManualBackupSerializer(serializers.Serializer):

    backup_scope = serializers.ChoiceField(
        choices=BackupLog.BackupScope.choices, default=BackupLog.BackupScope.DATABASE
    )

    notes = serializers.CharField(required=False, allow_blank=True)


# ============================================================
#                    RESTORE BACKUP SERIALIZER
# ============================================================


class RestoreBackupSerializer(serializers.Serializer):

    backup_id = serializers.IntegerField()

    def validate_backup_id(self, value):

        try:
            backup = BackupLog.objects.get(id=value)
        except BackupLog.DoesNotExist:
            raise serializers.ValidationError("Backup does not exist.")

        if backup.status not in [
            BackupLog.Status.SUCCESS,
            BackupLog.Status.RESTORED,
        ]:
            raise serializers.ValidationError(
                "Only successful backups can be restored."
            )

        return value


# ============================================================
#                    BACKUP HISTORY SERIALIZER
# ============================================================


class BackupHistorySerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(source="retailer.name", read_only=True)

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
            "restored_at",
        ]

        read_only_fields = [
            "id",
            "retailer_name",
            "backup_type",
            "backup_scope",
            "status",
            "file_name",
            "file_size",
            "created_at",
            "restored_at",
        ]


# ============================================================
#                    BACKUP SCHEDULE SERIALIZER
# ============================================================


class BackupScheduleSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(source="retailer.name", read_only=True)

    class Meta:
        model = BackupSchedule

        fields = [
            "id",
            "retailer",
            "retailer_name",
            "frequency",
            "backup_time",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "retailer_name",
            "created_at",
            "updated_at",
        ]

    def validate_backup_time(self, value):

        if value is None:
            raise serializers.ValidationError("Backup time is required.")

        return value
