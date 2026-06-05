from rest_framework import serializers
from .models import BackupLog

# ============================================================
#                      BACKUP SERIALIZERS   
# ============================================================
class BackupLogSerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(
        source="retailer.name",
        read_only=True
    )

    created_by_username = serializers.CharField(
        source="created_by.username",
        read_only=True
    )

    file_size_mb = serializers.SerializerMethodField()

    class Meta:
        model = BackupLog

        fields = [
            "id",
            "retailer",
            "retailer_name",
            "backup_type",
            "status",
            "file_name",
            "file_path",
            "file_size",
            "file_size_mb",
            "notes",
            "created_by",
            "created_by_username",
            "created_at",
            "restored_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "restored_at",
        ]

    def get_file_size_mb(self, obj):
        return round(obj.file_size / (1024 * 1024), 2)
    
# ============================================================
#                    MANUAL BACKUP SERIALIZERS
# ============================================================

class ManualBackupSerializer(serializers.Serializer):

    notes = serializers.CharField(
        required=False,
        allow_blank=True
    )

# ============================================================
#                   RESTORE BACKUP SERIALIZERS
# ============================================================

class RestoreBackupSerializer(serializers.Serializer):

    backup_id = serializers.IntegerField()

    def validate_backup_id(self, value):

        from .models import BackupLog

        if not BackupLog.objects.filter(
            id=value
        ).exists():

            raise serializers.ValidationError(
                "Backup does not exist"
            )

        return value
    
# ============================================================
#                   BACKUP HISTORY SERIALIZERS
# ============================================================

class BackupHistorySerializer(serializers.ModelSerializer):

    retailer_name = serializers.CharField(
        source="retailer.name",
        read_only=True
    )

    class Meta:
        model = BackupLog

        fields = [
            "id",
            "retailer_name",
            "backup_type",
            "status",
            "file_name",
            "created_at",
        ]

