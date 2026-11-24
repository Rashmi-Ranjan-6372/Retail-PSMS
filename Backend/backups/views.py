import hashlib
import logging
import shutil
import sqlite3
import tempfile
import zipfile

from pathlib import Path, PurePosixPath
from uuid import uuid4

from django.conf import settings
from django.db import connections
from django.db.models import F
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

logger = logging.getLogger(__name__)


# ============================================================
#                    BACKUP HELPER METHODS
# ============================================================


class BackupHelperMixin:

    def calculate_checksum(self, file_path):

        sha256 = hashlib.sha256()

        with open(file_path, "rb") as backup_file:

            for chunk in iter(
                lambda: backup_file.read(1024 * 1024),
                b"",
            ):
                sha256.update(chunk)

        return sha256.hexdigest()

    def create_database_backup(self, database_path, backup_path):

        source_connection = sqlite3.connect(str(database_path))

        try:

            backup_connection = sqlite3.connect(str(backup_path))

            try:
                source_connection.backup(backup_connection)

            finally:
                backup_connection.close()

        finally:
            source_connection.close()

    def validate_sqlite_database(self, database_path):

        connection = sqlite3.connect(str(database_path))

        try:

            result = connection.execute("PRAGMA integrity_check").fetchone()

            if not result or result[0] != "ok":
                raise ValueError("SQLite database integrity check failed.")

        finally:
            connection.close()

    def create_safety_backup(self, database_path, backup_root):

        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S_%f")

        safety_backup_path = backup_root / f"before_restore_{timestamp}.sqlite3"

        self.create_database_backup(
            database_path,
            safety_backup_path,
        )

        if not safety_backup_path.is_file():
            raise RuntimeError("Could not create safety backup.")

        return safety_backup_path

    def restore_sqlite_database(self, source_path, destination_path):

        self.validate_sqlite_database(source_path)

        # Close existing Django database connections.
        connections.close_all()

        source_connection = None
        destination_connection = None

        try:

            source_connection = sqlite3.connect(str(source_path))

            destination_connection = sqlite3.connect(str(destination_path))

            source_connection.backup(destination_connection)

            result = destination_connection.execute("PRAGMA integrity_check").fetchone()

            if not result or result[0] != "ok":
                raise ValueError("Restored database integrity check failed.")

        finally:

            if destination_connection:
                destination_connection.close()

            if source_connection:
                source_connection.close()

            connections.close_all()

    def validate_zip_archive(self, archive):

        for member in archive.infolist():

            member_path = PurePosixPath(member.filename)

            if (
                member_path.is_absolute()
                or ".." in member_path.parts
                or "\\" in member.filename
            ):
                raise ValueError("Backup archive contains an unsafe file path.")

            if member_path.parts and ":" in member_path.parts[0]:
                raise ValueError("Backup archive contains an unsafe file path.")

    def get_media_files(self):

        media_root = Path(settings.MEDIA_ROOT)

        backup_root = Path(
            getattr(
                settings,
                "BACKUP_ROOT",
                settings.BASE_DIR / "private_backups",
            )
        )

        if not media_root.exists():
            return

        media_root_resolved = media_root.resolve()
        backup_root_resolved = backup_root.resolve()

        backup_inside_media = (
            backup_root_resolved == media_root_resolved
            or media_root_resolved in backup_root_resolved.parents
        )

        for file_path in media_root.rglob("*"):

            if not file_path.is_file():
                continue

            if file_path.is_symlink():
                continue

            if backup_inside_media:

                try:
                    file_path.resolve().relative_to(backup_root_resolved)
                    continue

                except ValueError:
                    pass

            yield file_path

    def create_media_backup(self, backup_path):

        media_root = Path(settings.MEDIA_ROOT)

        with zipfile.ZipFile(
            backup_path,
            "w",
            compression=zipfile.ZIP_DEFLATED,
        ) as archive:

            if not media_root.exists():
                return

            for file_path in self.get_media_files():

                relative_path = file_path.relative_to(media_root)

                archive.write(
                    file_path,
                    arcname=str(relative_path),
                )

    def create_full_backup(self, database_path, backup_path):

        with tempfile.TemporaryDirectory() as temp_dir:

            temporary_database = Path(temp_dir) / "database.sqlite3"

            self.create_database_backup(
                database_path,
                temporary_database,
            )

            media_root = Path(settings.MEDIA_ROOT)

            with zipfile.ZipFile(
                backup_path,
                "w",
                compression=zipfile.ZIP_DEFLATED,
            ) as archive:

                archive.write(
                    temporary_database,
                    arcname="database/database.sqlite3",
                )

                if media_root.exists():

                    for file_path in self.get_media_files():

                        relative_path = file_path.relative_to(media_root)

                        archive.write(
                            file_path,
                            arcname=f"media/{relative_path}",
                        )

    def extract_media_archive(self, archive, destination):

        self.validate_zip_archive(archive)

        for member in archive.infolist():

            if member.is_dir():
                continue

            relative_path = PurePosixPath(member.filename)

            if not relative_path.parts:
                continue

            destination_path = destination.joinpath(*relative_path.parts)

            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with archive.open(member) as source:

                with open(destination_path, "wb") as target:
                    shutil.copyfileobj(source, target)

    def restore_media_files(self, source_root, media_root):

        media_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        for source_file in source_root.rglob("*"):

            if not source_file.is_file():
                continue

            relative_path = source_file.relative_to(source_root)

            destination_file = media_root / relative_path

            destination_file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                source_file,
                destination_file,
            )


# ============================================================
#                       CREATE BACKUP
# ============================================================


class CreateBackupView(BackupHelperMixin, APIView):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner,
    ]

    def post(self, request):

        if not request.user.is_superuser:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Only the Platform Owner can create " "application backups."
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ManualBackupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        backup_scope = serializer.validated_data.get(
            "backup_scope",
            BackupLog.BackupScope.DATABASE,
        )

        notes = serializer.validated_data.get("notes", "")

        database_config = settings.DATABASES["default"]

        database_path = None

        # Check database only for DATABASE and FULL backups.
        if backup_scope in [
            BackupLog.BackupScope.DATABASE,
            BackupLog.BackupScope.FULL,
        ]:

            if database_config["ENGINE"] != "django.db.backends.sqlite3":
                return Response(
                    {
                        "success": False,
                        "message": (
                            "Database backup currently supports " "SQLite only."
                        ),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            database_path = Path(database_config["NAME"])

            if not database_path.is_file():
                return Response(
                    {
                        "success": False,
                        "message": "Database file not found.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

        backup_dir = Path(
            getattr(
                settings,
                "BACKUP_ROOT",
                settings.BASE_DIR / "private_backups",
            )
        )

        backup_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S_%f")

        unique_id = uuid4().hex[:8]

        if backup_scope == BackupLog.BackupScope.DATABASE:

            backup_file = f"database_backup_{timestamp}_{unique_id}.sqlite3"

        elif backup_scope == BackupLog.BackupScope.MEDIA:

            backup_file = f"media_backup_{timestamp}_{unique_id}.zip"

        elif backup_scope == BackupLog.BackupScope.FULL:

            backup_file = f"full_backup_{timestamp}_{unique_id}.zip"

        else:

            return Response(
                {
                    "success": False,
                    "message": "Invalid backup scope.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        backup_path = backup_dir / backup_file

        backup = None

        try:

            backup = BackupLog.objects.create(
                retailer=None,
                backup_type=BackupLog.BackupType.MANUAL,
                backup_scope=backup_scope,
                status=BackupLog.Status.IN_PROGRESS,
                file_name=backup_file,
                notes=notes,
                created_by=request.user,
            )

            if backup_scope == BackupLog.BackupScope.DATABASE:

                self.create_database_backup(
                    database_path,
                    backup_path,
                )

            elif backup_scope == BackupLog.BackupScope.MEDIA:

                self.create_media_backup(backup_path)

            elif backup_scope == BackupLog.BackupScope.FULL:

                self.create_full_backup(
                    database_path,
                    backup_path,
                )

            if not backup_path.is_file():
                raise FileNotFoundError("Backup file was not created.")

            file_size = backup_path.stat().st_size

            if file_size == 0:
                raise ValueError("Generated backup file is empty.")

            checksum = self.calculate_checksum(backup_path)

            backup.file_path = str(backup_path)
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

        except Exception as error:

            if backup_path.exists():
                backup_path.unlink()

            if backup:

                backup.status = BackupLog.Status.FAILED
                backup.notes = str(error)

                backup.save(
                    update_fields=[
                        "status",
                        "notes",
                    ]
                )

            else:

                logger.exception("Backup log creation failed.")

            logger.exception("Backup creation failed.")

            return Response(
                {
                    "success": False,
                    "message": ("Backup creation failed. " "Please check server logs."),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:

            create_audit_log(
                user=request.user,
                action="create",
                model_name="BackupLog",
                object_id=backup.id,
                description=(
                    f"Created {backup.backup_scope} backup " f"{backup.file_name}"
                ),
                request=request,
            )

        except Exception:

            logger.exception("Backup audit log creation failed.")

        return Response(
            {
                "success": True,
                "message": "Backup created successfully.",
                "data": BackupLogSerializer(backup).data,
            },
            status=status.HTTP_201_CREATED,
        )


# ============================================================
#                       BACKUP HISTORY
# ============================================================


class BackupHistoryView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner,
    ]

    def get(self, request):

        if request.user.is_superuser:

            queryset = BackupLog.objects.all()

        else:

            queryset = BackupLog.objects.filter(retailer=request.user.retailer)

        queryset = queryset.order_by("-created_at")

        serializer = BackupHistorySerializer(
            queryset,
            many=True,
        )

        return Response(
            {
                "success": True,
                "count": queryset.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
#                       BACKUP DETAIL
# ============================================================


class BackupDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner,
    ]

    def get(self, request, pk):

        if request.user.is_superuser:

            backup = BackupLog.objects.filter(id=pk).first()

        else:

            backup = BackupLog.objects.filter(
                id=pk,
                retailer=request.user.retailer,
            ).first()

        if not backup:
            return Response(
                {
                    "success": False,
                    "message": "Backup not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "success": True,
                "data": BackupLogSerializer(backup).data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
#                       DOWNLOAD BACKUP
# ============================================================


class DownloadBackupView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner,
    ]

    def get(self, request, pk):

        if request.user.is_superuser:

            backup = BackupLog.objects.filter(id=pk).first()

        else:

            backup = BackupLog.objects.filter(
                id=pk,
                retailer=request.user.retailer,
            ).first()

        if not backup:
            return Response(
                {
                    "success": False,
                    "message": "Backup not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if backup.status not in [
            BackupLog.Status.SUCCESS,
            BackupLog.Status.RESTORED,
        ]:
            return Response(
                {
                    "success": False,
                    "message": "Only successful backups can be downloaded.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not backup.file_path:
            return Response(
                {
                    "success": False,
                    "message": "Backup file path unavailable.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        backup_path = Path(backup.file_path)

        if not backup_path.is_file():
            return Response(
                {
                    "success": False,
                    "message": "Backup file not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        BackupLog.objects.filter(id=backup.id).update(
            download_count=F("download_count") + 1
        )

        backup_file = open(backup_path, "rb")

        return FileResponse(
            backup_file,
            as_attachment=True,
            filename=backup.file_name,
        )


# ============================================================
#                       RESTORE BACKUP
# ============================================================


class RestoreBackupView(BackupHelperMixin, APIView):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner,
    ]

    def post(self, request):

        if not request.user.is_superuser:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Only the Platform Owner can restore " "application backups."
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = RestoreBackupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        backup_id = serializer.validated_data["backup_id"]

        backup = BackupLog.objects.filter(
            id=backup_id,
            retailer__isnull=True,
            status__in=[
                BackupLog.Status.SUCCESS,
                BackupLog.Status.RESTORED,
            ],
        ).first()

        if not backup:
            return Response(
                {
                    "success": False,
                    "message": "Successful backup not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if not backup.file_path:
            return Response(
                {
                    "success": False,
                    "message": "Backup file path unavailable.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        backup_path = Path(backup.file_path)

        if not backup_path.is_file():
            return Response(
                {
                    "success": False,
                    "message": "Backup file not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:

            if backup.checksum:

                calculated_checksum = self.calculate_checksum(backup_path)

                if calculated_checksum != backup.checksum:
                    return Response(
                        {
                            "success": False,
                            "message": (
                                "Backup checksum verification failed. "
                                "The backup file may be corrupted."
                            ),
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            database_config = settings.DATABASES["default"]

            database_path = Path(database_config["NAME"])

            backup_root = Path(
                getattr(
                    settings,
                    "BACKUP_ROOT",
                    settings.BASE_DIR / "private_backups",
                )
            )

            backup_root.mkdir(
                parents=True,
                exist_ok=True,
            )

            media_root = Path(settings.MEDIA_ROOT)

            backup_scope = backup.backup_scope

            if backup_scope == BackupLog.BackupScope.DATABASE:

                if database_config["ENGINE"] != "django.db.backends.sqlite3":
                    return Response(
                        {
                            "success": False,
                            "message": (
                                "Database restoration currently "
                                "supports SQLite only."
                            ),
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not database_path.is_file():
                    return Response(
                        {
                            "success": False,
                            "message": "Current database file not found.",
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )

                self.validate_sqlite_database(backup_path)

                self.create_safety_backup(
                    database_path,
                    backup_root,
                )

                self.restore_sqlite_database(
                    backup_path,
                    database_path,
                )

                message = (
                    "Database restored successfully. "
                    "A safety backup of the previous database was created."
                )

            elif backup_scope == BackupLog.BackupScope.MEDIA:

                with tempfile.TemporaryDirectory() as temp_dir:

                    extracted_media = Path(temp_dir) / "media"

                    extracted_media.mkdir(
                        parents=True,
                        exist_ok=True,
                    )

                    with zipfile.ZipFile(
                        backup_path,
                        "r",
                    ) as archive:

                        self.extract_media_archive(
                            archive,
                            extracted_media,
                        )

                    self.restore_media_files(
                        extracted_media,
                        media_root,
                    )

                message = "Media files restored successfully."

            elif backup_scope == BackupLog.BackupScope.FULL:

                if database_config["ENGINE"] != "django.db.backends.sqlite3":
                    return Response(
                        {
                            "success": False,
                            "message": (
                                "Database restoration currently "
                                "supports SQLite only."
                            ),
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not database_path.is_file():
                    return Response(
                        {
                            "success": False,
                            "message": "Current database file not found.",
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )

                with tempfile.TemporaryDirectory() as temp_dir:

                    temp_root = Path(temp_dir)

                    extracted_database = temp_root / "database.sqlite3"

                    extracted_media = temp_root / "media"

                    extracted_media.mkdir(
                        parents=True,
                        exist_ok=True,
                    )

                    with zipfile.ZipFile(
                        backup_path,
                        "r",
                    ) as archive:

                        self.validate_zip_archive(archive)

                        database_member = "database/database.sqlite3"

                        if database_member not in archive.namelist():
                            raise ValueError(
                                "Database file is missing from full backup."
                            )

                        with archive.open(database_member) as source:

                            with open(
                                extracted_database,
                                "wb",
                            ) as destination:

                                shutil.copyfileobj(
                                    source,
                                    destination,
                                )

                        for member in archive.infolist():

                            if not member.filename.startswith("media/"):
                                continue

                            if member.is_dir():
                                continue

                            relative_path = PurePosixPath(
                                member.filename[len("media/") :]
                            )

                            if not relative_path.parts:
                                continue

                            destination_path = extracted_media.joinpath(
                                *relative_path.parts
                            )

                            destination_path.parent.mkdir(
                                parents=True,
                                exist_ok=True,
                            )

                            with archive.open(member) as source:

                                with open(
                                    destination_path,
                                    "wb",
                                ) as destination:

                                    shutil.copyfileobj(
                                        source,
                                        destination,
                                    )

                    self.validate_sqlite_database(extracted_database)

                    self.create_safety_backup(
                        database_path,
                        backup_root,
                    )

                    self.restore_sqlite_database(
                        extracted_database,
                        database_path,
                    )

                    self.restore_media_files(
                        extracted_media,
                        media_root,
                    )

                message = (
                    "Full application backup restored successfully. "
                    "A safety backup of the previous database was created."
                )

            else:

                return Response(
                    {
                        "success": False,
                        "message": "Unsupported backup scope.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            backup.status = BackupLog.Status.RESTORED
            backup.restored_at = timezone.now()
            backup.restored_by = request.user

            backup.save(
                update_fields=[
                    "status",
                    "restored_at",
                    "restored_by",
                ]
            )

            try:

                create_audit_log(
                    user=request.user,
                    action="update",
                    model_name="BackupLog",
                    object_id=backup.id,
                    description=(
                        f"Restored {backup.backup_scope} backup: " f"{backup.file_name}"
                    ),
                    request=request,
                )

            except Exception:

                logger.exception("Backup restoration audit log failed.")

            return Response(
                {
                    "success": True,
                    "message": message,
                    "data": BackupLogSerializer(backup).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception:

            logger.exception("Backup restoration failed.")

            return Response(
                {
                    "success": False,
                    "message": (
                        "Backup restoration failed. " "Check server logs for details."
                    ),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ============================================================
#                       BACKUP SCHEDULE
# ============================================================


class BackupScheduleView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner,
    ]

    def get(self, request):

        if request.user.is_superuser:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Platform Owner does not have a "
                        "retailer-specific backup schedule."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        schedule = BackupSchedule.objects.filter(retailer=request.user.retailer).first()

        if not schedule:
            return Response(
                {
                    "success": False,
                    "message": "Backup schedule not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BackupScheduleSerializer(schedule)

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):

        if request.user.is_superuser:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Platform Owner cannot create a retailer "
                        "schedule without specifying a retailer."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        check_subscription_write_access(request.user.retailer)

        schedule = BackupSchedule.objects.filter(retailer=request.user.retailer).first()

        if schedule:

            serializer = BackupScheduleSerializer(
                schedule,
                data=request.data,
                partial=True,
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
                "message": (f"Backup schedule {action} successfully."),
                "data": BackupScheduleSerializer(backup_schedule).data,
            },
            status=(
                status.HTTP_200_OK if action == "updated" else status.HTTP_201_CREATED
            ),
        )
