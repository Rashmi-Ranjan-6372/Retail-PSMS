import os
import shutil
from datetime import datetime

from django.conf import settings
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import BackupLog
from .serializers import (
    BackupLogSerializer,
    BackupHistorySerializer,
    ManualBackupSerializer,
    RestoreBackupSerializer,
)
from accounts.permissions import IsRetailerOwnerOrPlatformOwner

# ============================================================
#                     BACKUP VIEWS
# ============================================================
class CreateBackupView(APIView):
    permission_classes = [IsRetailerOwnerOrPlatformOwner]
    def post(self, request):

        serializer = ManualBackupSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        backup_dir = os.path.join(
            settings.MEDIA_ROOT,
            "backups"
        )

        os.makedirs(
            backup_dir,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_file = (
            f"backup_{timestamp}.sqlite3"
        )

        backup_path = os.path.join(
            backup_dir,
            backup_file
        )

        try:

            shutil.copy2(
                settings.DATABASES["default"]["NAME"],
                backup_path
            )

            file_size = os.path.getsize(
                backup_path
            )

            backup = BackupLog.objects.create(
                retailer=request.user.retailer,
                backup_type="manual",
                status="success",
                file_name=backup_file,
                file_path=backup_path,
                file_size=file_size,
                notes=serializer.validated_data.get(
                    "notes"
                ),
                created_by=request.user
            )

            return Response(
                {
                    "success": True,
                    "message": "Backup created successfully",
                    "data": BackupLogSerializer(
                        backup
                    ).data
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            BackupLog.objects.create(
                retailer=request.user.retailer,
                backup_type="manual",
                status="failed",
                file_name=backup_file,
                notes=str(e),
                created_by=request.user
            )

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ============================================================
#                    BACKUP HISTORY VIEWS
# ============================================================
class BackupHistoryView(APIView):
    permission_classes = [IsRetailerOwnerOrPlatformOwner]

    def get(self, request):

        queryset = BackupLog.objects.filter(
            retailer=request.user.retailer
        )

        serializer = BackupHistorySerializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,
                "count": queryset.count(),
                "data": serializer.data
            }
        )

# ============================================================
#                    BACKUP DETAIL VIEWS
# ============================================================
class BackupDetailView(APIView):
    permission_classes = [IsRetailerOwnerOrPlatformOwner]

    def get(self, request, pk):

        try:

            backup = BackupLog.objects.get(
                id=pk,
                retailer=request.user.retailer
            )

        except BackupLog.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Backup not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,
                "data": BackupLogSerializer(
                    backup
                ).data
            }
        )

# ============================================================
#                   RESTORE BACKUP VIEWS
# ============================================================
class RestoreBackupView(APIView):
    permission_classes = [IsRetailerOwnerOrPlatformOwner]

    def post(self, request):

        serializer = RestoreBackupSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        backup_id = serializer.validated_data[
            "backup_id"
        ]

        try:

            backup = BackupLog.objects.get(
                id=backup_id,
                retailer=request.user.retailer
            )

        except BackupLog.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Backup not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not os.path.exists(
            backup.file_path
        ):
            return Response(
                {
                    "success": False,
                    "message": "Backup file not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            shutil.copy2(
                backup.file_path,
                settings.DATABASES["default"]["NAME"]
            )

            backup.status = "restored"
            backup.restored_at = timezone.now()

            backup.save(
                update_fields=[
                    "status",
                    "restored_at"
                ]
            )

            return Response(
                {
                    "success": True,
                    "message": "Database restored successfully"
                }
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )