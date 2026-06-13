import os
import shutil

from django.conf import settings
from django.utils import timezone

from subscriptions.utils import (
    check_subscription_write_access
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse

from .models import BackupLog, BackupSchedule
from .serializers import (
    BackupLogSerializer,
    BackupHistorySerializer,
    ManualBackupSerializer,
    RestoreBackupSerializer,
    BackupScheduleSerializer
)

from accounts.permissions import (
    IsRetailerOwnerOrPlatformOwner
)

from accounts.views import create_audit_log


# ============================================================
#                     CREATE BACKUP
# ============================================================
class CreateBackupView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner
    ]

    def post(self, request):

        if not request.user.is_superuser:

            check_subscription_write_access(
                request.user.retailer
            )

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

        timestamp = timezone.now().strftime(
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
                backup_scope="database",
                status="success",
                file_name=backup_file,
                file_path=backup_path,
                file_size=file_size,
                notes=serializer.validated_data.get(
                    "notes"
                ),
                created_by=request.user
            )

            create_audit_log(
                user=request.user,
                action="create",
                model_name="Backup",
                object_id=backup.id,
                description=(
                    f"Created backup "
                    f"{backup.file_name}"
                ),
                request=request
            )

            return Response(
                {
                    "success": True,
                    "message": (
                        "Backup created successfully"
                    ),
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
#                     BACKUP HISTORY
# ============================================================
class BackupHistoryView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner
    ]

    def get(self, request):

        if request.user.is_superuser:

            queryset = BackupLog.objects.all()

        else:

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
            },
            status=status.HTTP_200_OK
        )


# ============================================================
#                     BACKUP DETAIL
# ============================================================
class BackupDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner
    ]

    def get(self, request, pk):

        try:

            if request.user.is_superuser:

                backup = BackupLog.objects.get(
                    id=pk
                )

            else:

                backup = BackupLog.objects.get(
                    id=pk,
                    retailer=request.user.retailer
                )

        except BackupLog.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Backup not found"
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,
                "data": BackupLogSerializer(
                    backup
                ).data
            },
            status=status.HTTP_200_OK
        )


# ============================================================
#                     DOWNLOAD BACKUP
# ============================================================
class DownloadBackupView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner
    ]

    def get(self, request, pk):

        try:

            if request.user.is_superuser:

                backup = BackupLog.objects.get(
                    id=pk
                )

            else:

                backup = BackupLog.objects.get(
                    id=pk,
                    retailer=request.user.retailer
                )

        except BackupLog.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Backup not found"
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not backup.file_path:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Backup file unavailable"
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not os.path.exists(
            backup.file_path
        ):

            return Response(
                {
                    "success": False,
                    "message": (
                        "Backup file not found"
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        backup.download_count += 1

        backup.save(
            update_fields=[
                "download_count"
            ]
        )

        return FileResponse(
            open(
                backup.file_path,
                "rb"
            ),
            as_attachment=True,
            filename=backup.file_name
        )


# ============================================================
#                     RESTORE BACKUP
# ============================================================
class RestoreBackupView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner
    ]

    def post(self, request):

        if not request.user.is_superuser:

            check_subscription_write_access(
                request.user.retailer
            )

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

            if request.user.is_superuser:

                backup = BackupLog.objects.get(
                    id=backup_id
                )

            else:

                backup = BackupLog.objects.get(
                    id=backup_id,
                    retailer=request.user.retailer
                )

        except BackupLog.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Backup not found"
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if backup.status == "failed":

            return Response(
                {
                    "success": False,
                    "message": (
                        "Cannot restore "
                        "a failed backup"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not backup.file_path:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Backup file unavailable"
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not os.path.exists(
            backup.file_path
        ):

            return Response(
                {
                    "success": False,
                    "message": (
                        "Backup file not found"
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            shutil.copy2(
                backup.file_path,
                settings.DATABASES[
                    "default"
                ]["NAME"]
            )

            backup.status = "restored"

            backup.restored_at = (
                timezone.now()
            )

            backup.restored_by = (
                request.user
            )

            backup.save(
                update_fields=[
                    "status",
                    "restored_at",
                    "restored_by"
                ]
            )

            create_audit_log(
                user=request.user,
                action="update",
                model_name="Backup",
                object_id=backup.id,
                description=(
                    f"Restored backup "
                    f"{backup.file_name}"
                ),
                request=request
            )

            return Response(
                {
                    "success": True,
                    "message": (
                        "Database restored "
                        "successfully"
                    )
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ============================================================
#                   BACKUP SCHEDULE VIEW
# ============================================================
class BackupScheduleView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner
    ]

    def get(self, request):

        schedule = BackupSchedule.objects.filter(
            retailer=request.user.retailer
        ).first()

        if not schedule:

            return Response(
                {
                    "success": False,
                    "message": "Backup schedule not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BackupScheduleSerializer(
            schedule
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):

        if not request.user.is_superuser:

            check_subscription_write_access(
                request.user.retailer
            )

        schedule = BackupSchedule.objects.filter(
            retailer=request.user.retailer
        ).first()

        if schedule:

            serializer = BackupScheduleSerializer(
                schedule,
                data=request.data,
                partial=True
            )

            action = "updated"

        else:

            serializer = BackupScheduleSerializer(
                data=request.data
            )

            action = "created"

        serializer.is_valid(
            raise_exception=True
        )

        backup_schedule = serializer.save(
            retailer=request.user.retailer
        )

        create_audit_log(
            user=request.user,
            action="update" if action == "updated" else "create",
            model_name="BackupSchedule",
            object_id=backup_schedule.id,
            description=(
                f"{action.capitalize()} backup schedule "
                f"({backup_schedule.frequency})"
            ),
            request=request
        )

        return Response(
            {
                "success": True,
                "message": (
                    f"Backup schedule {action} successfully"
                ),
                "data": BackupScheduleSerializer(
                    backup_schedule
                ).data
            },
            status=status.HTTP_200_OK
        )