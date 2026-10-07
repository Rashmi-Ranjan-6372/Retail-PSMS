import hashlib
import os
import shutil

from django.conf import settings
from django.http import FileResponse
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from subscriptions.utils import check_subscription_write_access

from .models import BackupLog, BackupSchedule

from .serializers import (
    BackupLogSerializer,
    BackupHistorySerializer,
    ManualBackupSerializer,
    RestoreBackupSerializer,
    BackupScheduleSerializer,
)

from accounts.permissions import IsRetailerOwnerOrPlatformOwner

from accounts.views import create_audit_log

# ============================================================
#                     CREATE BACKUP
# ============================================================


class CreateBackupView(APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    def post(self, request):

        if not request.user.is_superuser:
            check_subscription_write_access(request.user.retailer)

        serializer = ManualBackupSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        backup_scope = serializer.validated_data.get(
            "backup_scope", BackupLog.BackupScope.DATABASE
        )

        notes = serializer.validated_data.get("notes", "")

        backup_dir = os.path.join(settings.MEDIA_ROOT, "backups")

        os.makedirs(backup_dir, exist_ok=True)

        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")

        backup_file = f"backup_{timestamp}.sqlite3"

        backup_path = os.path.join(backup_dir, backup_file)

        backup = None

        try:

            backup = BackupLog.objects.create(
                retailer=(
                    request.user.retailer if not request.user.is_superuser else None
                ),
                backup_type=BackupLog.BackupType.MANUAL,
                backup_scope=backup_scope,
                status=BackupLog.Status.IN_PROGRESS,
                file_name=backup_file,
                notes=notes,
                created_by=request.user,
            )

            shutil.copy2(settings.DATABASES["default"]["NAME"], backup_path)

            file_size = os.path.getsize(backup_path)

            checksum = self.calculate_checksum(backup_path)

            backup.file_path = backup_path
            backup.file_size = file_size
            backup.checksum = checksum
            backup.status = BackupLog.Status.SUCCESS

            backup.save(
                update_fields=[
                    "file_path",
                    "file_size",
                    "checksum",
                    "status",
                ]
            )

            create_audit_log(
                user=request.user,
                action="create",
                model_name="BackupLog",
                object_id=backup.id,
                description=(f"Created backup " f"{backup.file_name}"),
                request=request,
            )

            return Response(
                {
                    "success": True,
                    "message": ("Backup created successfully"),
                    "data": BackupLogSerializer(backup).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:

            if backup:

                backup.status = BackupLog.Status.FAILED
                backup.notes = str(e)
                backup.save(update_fields=["status", "notes"])

            else:

                BackupLog.objects.create(
                    retailer=(
                        request.user.retailer if not request.user.is_superuser else None
                    ),
                    backup_type=BackupLog.BackupType.MANUAL,
                    backup_scope=backup_scope,
                    status=BackupLog.Status.FAILED,
                    file_name=backup_file,
                    notes=str(e),
                    created_by=request.user,
                )

            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def calculate_checksum(self, file_path):

        sha256 = hashlib.sha256()

        with open(file_path, "rb") as backup_file:

            for chunk in iter(lambda: backup_file.read(1024 * 1024), b""):
                sha256.update(chunk)

        return sha256.hexdigest()


# ============================================================
#                     BACKUP HISTORY
# ============================================================


class BackupHistoryView(APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    def get(self, request):

        if request.user.is_superuser:

            queryset = BackupLog.objects.all()

        else:

            queryset = BackupLog.objects.filter(retailer=request.user.retailer)

        queryset = queryset.order_by("-created_at")

        serializer = BackupHistorySerializer(queryset, many=True)

        return Response(
            {"success": True, "count": queryset.count(), "data": serializer.data},
            status=status.HTTP_200_OK,
        )


# ============================================================
#                     BACKUP DETAIL
# ============================================================


class BackupDetailView(APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    def get(self, request, pk):

        if request.user.is_superuser:

            backup = BackupLog.objects.filter(id=pk).first()

        else:

            backup = BackupLog.objects.filter(
                id=pk, retailer=request.user.retailer
            ).first()

        if not backup:

            return Response(
                {"success": False, "message": "Backup not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"success": True, "data": BackupLogSerializer(backup).data},
            status=status.HTTP_200_OK,
        )


# ============================================================
#                     DOWNLOAD BACKUP
# ============================================================


class DownloadBackupView(APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    def get(self, request, pk):

        if request.user.is_superuser:

            backup = BackupLog.objects.filter(id=pk).first()

        else:

            backup = BackupLog.objects.filter(
                id=pk, retailer=request.user.retailer
            ).first()

        if not backup:

            return Response(
                {"success": False, "message": "Backup not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if backup.status not in [BackupLog.Status.SUCCESS, BackupLog.Status.RESTORED]:

            return Response(
                {
                    "success": False,
                    "message": ("Only successful backups " "can be downloaded"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not backup.file_path:

            return Response(
                {"success": False, "message": "Backup file unavailable"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not os.path.exists(backup.file_path):

            return Response(
                {"success": False, "message": "Backup file not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        backup.download_count += 1

        backup.save(update_fields=["download_count"])

        return FileResponse(
            open(backup.file_path, "rb"), as_attachment=True, filename=backup.file_name
        )


# ============================================================
#                     RESTORE BACKUP
# ============================================================


class RestoreBackupView(APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    def post(self, request):

        if not request.user.is_superuser:
            check_subscription_write_access(request.user.retailer)

        serializer = RestoreBackupSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        backup_id = serializer.validated_data["backup_id"]

        if request.user.is_superuser:

            backup = BackupLog.objects.filter(id=backup_id).first()

        else:

            backup = BackupLog.objects.filter(
                id=backup_id, retailer=request.user.retailer
            ).first()

        if not backup:

            return Response(
                {"success": False, "message": "Backup not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if backup.status not in [BackupLog.Status.SUCCESS, BackupLog.Status.RESTORED]:

            return Response(
                {
                    "success": False,
                    "message": ("Only successful backups " "can be restored"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not backup.file_path:

            return Response(
                {"success": False, "message": "Backup file unavailable"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not os.path.exists(backup.file_path):

            return Response(
                {"success": False, "message": "Backup file not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:

            database_path = settings.DATABASES["default"]["NAME"]

            shutil.copy2(backup.file_path, database_path)

            backup.status = BackupLog.Status.RESTORED
            backup.restored_at = timezone.now()
            backup.restored_by = request.user

            backup.save(update_fields=["status", "restored_at", "restored_by"])

            create_audit_log(
                user=request.user,
                action="update",
                model_name="BackupLog",
                object_id=backup.id,
                description=(f"Restored backup " f"{backup.file_name}"),
                request=request,
            )

            return Response(
                {
                    "success": True,
                    "message": ("Database restored successfully"),
                    "data": BackupLogSerializer(backup).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ============================================================
#                   BACKUP SCHEDULE VIEW
# ============================================================


class BackupScheduleView(APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    def get(self, request):

        if request.user.is_superuser:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Platform Owner does not have "
                        "a retailer-specific backup schedule"
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        schedule = BackupSchedule.objects.filter(retailer=request.user.retailer).first()

        if not schedule:

            return Response(
                {"success": False, "message": "Backup schedule not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BackupScheduleSerializer(schedule)

        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request):

        if request.user.is_superuser:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Platform Owner cannot create "
                        "a retailer schedule without "
                        "specifying a retailer"
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        check_subscription_write_access(request.user.retailer)

        schedule = BackupSchedule.objects.filter(retailer=request.user.retailer).first()

        if schedule:

            serializer = BackupScheduleSerializer(
                schedule, data=request.data, partial=True
            )

            action = "updated"

        else:

            serializer = BackupScheduleSerializer(data=request.data)

            action = "created"

        serializer.is_valid(raise_exception=True)

        backup_schedule = serializer.save(retailer=request.user.retailer)

        create_audit_log(
            user=request.user,
            action=("update" if action == "updated" else "create"),
            model_name="BackupSchedule",
            object_id=backup_schedule.id,
            description=(
                f"{action.capitalize()} backup schedule "
                f"({backup_schedule.frequency})"
            ),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": (f"Backup schedule " f"{action} successfully"),
                "data": BackupScheduleSerializer(backup_schedule).data,
            },
            status=(
                status.HTTP_200_OK if action == "updated" else status.HTTP_201_CREATED
            ),
        )
