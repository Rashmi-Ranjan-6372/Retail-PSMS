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
# BACKUP HELPER METHODS
# ============================================================


class BackupHelperMixin:

    # ========================================================
    # BACKUP DIRECTORY
    # ========================================================

    def get_backup_root(self):

        backup_root = Path(
            getattr(
                settings,
                "BACKUP_ROOT",
                Path(settings.BASE_DIR) / "private_backups",
            )
        ).resolve()

        backup_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        return backup_root

    # ========================================================
    # SAFE BACKUP FILE PATH
    # ========================================================

    def get_safe_backup_path(self, backup):

        if not backup.file_path:
            raise ValueError("Backup file path is missing.")

        original_path = Path(backup.file_path)

        if original_path.is_symlink():
            raise ValueError("Symbolic links are not allowed.")

        backup_root = self.get_backup_root()

        backup_path = original_path.resolve()

        try:
            backup_path.relative_to(backup_root)
        except ValueError:
            raise ValueError("Backup file is outside the configured backup directory.")

        if not backup_path.is_file():
            raise FileNotFoundError("Backup file does not exist.")

        return backup_path

    # ========================================================
    # CHECKSUM
    # ========================================================

    def calculate_checksum(self, file_path):

        sha256 = hashlib.sha256()

        with open(file_path, "rb") as backup_file:

            for chunk in iter(
                lambda: backup_file.read(1024 * 1024),
                b"",
            ):
                sha256.update(chunk)

        return sha256.hexdigest()

    def verify_backup_checksum(self, backup, backup_path):

        if not backup.checksum:
            raise ValueError("Backup checksum is missing.")

        calculated_checksum = self.calculate_checksum(backup_path)

        if calculated_checksum != backup.checksum:
            raise ValueError("Backup checksum verification failed.")

        return True

    # ========================================================
    # DATABASE PATH
    # ========================================================

    def get_database_path(self):

        database_config = settings.DATABASES["default"]

        if database_config["ENGINE"] != "django.db.backends.sqlite3":
            raise ValueError(
                "This backup implementation currently supports SQLite only."
            )

        database_path = Path(database_config["NAME"]).resolve()

        if not database_path.is_file():
            raise FileNotFoundError("Database file not found.")

        return database_path

    # ========================================================
    # CREATE DATABASE BACKUP
    # ========================================================

    def create_database_backup(
        self,
        database_path,
        backup_path,
    ):

        source_connection = sqlite3.connect(str(database_path))

        try:

            backup_connection = sqlite3.connect(str(backup_path))

            try:

                source_connection.backup(backup_connection)

                result = backup_connection.execute("PRAGMA integrity_check").fetchone()

                if not result or result[0] != "ok":
                    raise ValueError("Database backup integrity check failed.")

            finally:
                backup_connection.close()

        finally:
            source_connection.close()

    # ========================================================
    # VALIDATE SQLITE DATABASE
    # ========================================================

    def validate_sqlite_database(self, database_path):

        if not Path(database_path).is_file():
            raise FileNotFoundError("SQLite database file does not exist.")

        connection = sqlite3.connect(str(database_path))

        try:

            result = connection.execute("PRAGMA integrity_check").fetchone()

            if not result or result[0] != "ok":
                raise ValueError("SQLite database integrity check failed.")

        finally:
            connection.close()

    # ========================================================
    # CREATE SAFETY DATABASE BACKUP
    # ========================================================

    def create_safety_backup(
        self,
        database_path,
        backup_root,
    ):

        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S_%f")

        safety_backup_path = backup_root / f"before_restore_{timestamp}.sqlite3"

        self.create_database_backup(
            database_path,
            safety_backup_path,
        )

        if not safety_backup_path.is_file():
            raise RuntimeError("Could not create safety backup.")

        return safety_backup_path

    # ========================================================
    # RESTORE SQLITE DATABASE
    # ========================================================

    def restore_sqlite_database(
        self,
        source_path,
        destination_path,
    ):

        self.validate_sqlite_database(source_path)

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

    # ========================================================
    # VALIDATE ZIP ARCHIVE
    # ========================================================

    def validate_zip_archive(self, archive):

        total_uncompressed_size = 0

        max_uncompressed_size = 10 * 1024 * 1024 * 1024

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

            unix_mode = member.external_attr >> 16

            if (unix_mode & 0o170000) == 0o120000:
                raise ValueError("Symbolic links are not allowed in backup archives.")

            total_uncompressed_size += member.file_size

            if total_uncompressed_size > max_uncompressed_size:
                raise ValueError("Backup archive exceeds the maximum allowed size.")

    # ========================================================
    # GET MEDIA FILES
    # ========================================================

    def get_media_files(self):

        media_root = Path(settings.MEDIA_ROOT).resolve()

        backup_root = self.get_backup_root()

        if not media_root.exists():
            return

        backup_inside_media = (
            backup_root == media_root or media_root in backup_root.parents
        )

        for file_path in media_root.rglob("*"):

            if file_path.is_symlink():
                continue

            if not file_path.is_file():
                continue

            if backup_inside_media:

                try:
                    file_path.resolve().relative_to(backup_root)
                    continue

                except ValueError:
                    pass

            yield file_path

    # ========================================================
    # CREATE MEDIA BACKUP
    # ========================================================

    def create_media_backup(self, backup_path):

        media_root = Path(settings.MEDIA_ROOT).resolve()

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

    # ========================================================
    # CREATE FULL BACKUP
    # ========================================================

    def create_full_backup(
        self,
        database_path,
        backup_path,
    ):

        with tempfile.TemporaryDirectory() as temp_dir:

            temporary_database = Path(temp_dir) / "database.sqlite3"

            self.create_database_backup(
                database_path,
                temporary_database,
            )

            media_root = Path(settings.MEDIA_ROOT).resolve()

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

    # ========================================================
    # CREATE PLATFORM BACKUP
    # ========================================================

    def create_platform_backup(
        self,
        backup_scope,
        backup_type=BackupLog.BackupType.AUTOMATIC,
        created_by=None,
        notes="",
    ):

        if backup_scope not in BackupLog.BackupScope.values:
            raise ValueError("Unsupported backup scope.")

        database_path = None

        if backup_scope in [
            BackupLog.BackupScope.DATABASE,
            BackupLog.BackupScope.FULL,
        ]:
            database_path = self.get_database_path()

        backup_dir = self.get_backup_root()

        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S_%f")

        unique_id = uuid4().hex[:8]

        file_extensions = {
            BackupLog.BackupScope.DATABASE: ".sqlite3",
            BackupLog.BackupScope.MEDIA: ".zip",
            BackupLog.BackupScope.FULL: ".zip",
        }

        file_name = (
            f"{backup_scope}_backup_"
            f"{timestamp}_{unique_id}"
            f"{file_extensions[backup_scope]}"
        )

        backup_path = backup_dir / file_name

        backup = BackupLog.objects.create(
            retailer=None,
            backup_type=backup_type,
            backup_scope=backup_scope,
            status=BackupLog.Status.IN_PROGRESS,
            file_name=file_name,
            notes=notes,
            created_by=created_by,
        )

        try:

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
                    "updated_at",
                ]
            )

            return backup

        except Exception as error:

            if backup_path.exists():
                backup_path.unlink()

            backup.status = BackupLog.Status.FAILED

            backup.notes = (f"{notes}\nError: {str(error)}").strip()

            backup.save(
                update_fields=[
                    "status",
                    "notes",
                    "updated_at",
                ]
            )

            logger.exception("Platform backup creation failed.")

            raise

    # ========================================================
    # EXTRACT MEDIA ARCHIVE
    # ========================================================

    def extract_media_archive(
        self,
        archive,
        destination,
    ):

        self.validate_zip_archive(archive)

        destination = destination.resolve()

        for member in archive.infolist():

            if member.is_dir():
                continue

            relative_path = PurePosixPath(member.filename)

            if not relative_path.parts:
                continue

            destination_path = (destination.joinpath(*relative_path.parts)).resolve()

            try:
                destination_path.relative_to(destination)
            except ValueError:
                raise ValueError("Unsafe archive extraction path.")

            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with archive.open(member) as source:

                with open(
                    destination_path,
                    "wb",
                ) as target:

                    shutil.copyfileobj(
                        source,
                        target,
                    )

    # ========================================================
    # RESTORE MEDIA FILES
    # ========================================================

    def restore_media_files(
        self,
        source_root,
        media_root,
    ):

        source_root = Path(source_root).resolve()

        media_root = Path(media_root).resolve()

        media_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        for source_file in source_root.rglob("*"):

            if source_file.is_symlink():
                continue

            if not source_file.is_file():
                continue

            relative_path = source_file.relative_to(source_root)

            destination_file = (media_root / relative_path).resolve()

            try:
                destination_file.relative_to(media_root)
            except ValueError:
                raise ValueError("Unsafe media restoration path.")

            destination_file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                source_file,
                destination_file,
            )

    # ========================================================
    # AUDIT LOG
    # ========================================================

    def record_audit_log(
        self,
        request,
        action,
        model_name,
        object_id,
        description,
    ):

        try:

            create_audit_log(
                user=request.user,
                action=action,
                model_name=model_name,
                object_id=object_id,
                description=description,
                request=request,
            )

        except Exception:

            logger.exception("Backup audit log creation failed.")

    # ========================================================
    # GET ACCESSIBLE BACKUP
    # ========================================================

    def get_accessible_backup(
        self,
        request,
        pk,
    ):

        if not request.user.is_superuser:
            return None

        return BackupLog.objects.filter(
            id=pk,
            retailer__isnull=True,
        ).first()


# ============================================================
# CREATE BACKUP
# ============================================================


class CreateBackupView(
    BackupHelperMixin,
    APIView,
):

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

        notes = serializer.validated_data.get(
            "notes",
            "",
        )

        try:

            backup = self.create_platform_backup(
                backup_scope=backup_scope,
                backup_type=BackupLog.BackupType.MANUAL,
                created_by=request.user,
                notes=notes,
            )

        except (ValueError, FileNotFoundError) as error:

            logger.exception("Invalid platform backup request.")

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception:

            logger.exception("Manual platform backup failed.")

            return Response(
                {
                    "success": False,
                    "message": ("Backup creation failed. " "Please check server logs."),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        self.record_audit_log(
            request=request,
            action="create",
            model_name="BackupLog",
            object_id=backup.id,
            description=(
                f"Created {backup.backup_scope} backup " f"{backup.file_name}"
            ),
        )

        return Response(
            {
                "success": True,
                "message": "Backup created successfully.",
                "data": BackupLogSerializer(backup).data,
            },
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# BACKUP HISTORY
# ============================================================


class BackupHistoryView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner,
    ]

    def get(self, request):

        if not request.user.is_superuser:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Only the Platform Owner can view "
                        "application backup history."
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        queryset = BackupLog.objects.filter(retailer__isnull=True).order_by(
            "-created_at"
        )

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
# BACKUP DETAIL
# ============================================================


class BackupDetailView(
    BackupHelperMixin,
    APIView,
):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner,
    ]

    def get(self, request, pk):

        backup = self.get_accessible_backup(
            request,
            pk,
        )

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
# DOWNLOAD BACKUP
# ============================================================


class DownloadBackupView(
    BackupHelperMixin,
    APIView,
):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner,
    ]

    def get(self, request, pk):

        backup = self.get_accessible_backup(
            request,
            pk,
        )

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
                    "message": ("Only successful backups can be downloaded."),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            backup_path = self.get_safe_backup_path(backup)

            self.verify_backup_checksum(
                backup,
                backup_path,
            )

        except (ValueError, FileNotFoundError) as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        BackupLog.objects.filter(id=backup.id).update(
            download_count=F("download_count") + 1
        )

        backup_file = open(
            backup_path,
            "rb",
        )

        return FileResponse(
            backup_file,
            as_attachment=True,
            filename=backup.file_name,
        )


# ============================================================
# RESTORE BACKUP
# ============================================================


class RestoreBackupView(
    BackupHelperMixin,
    APIView,
):

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

        try:

            backup_path = self.get_safe_backup_path(backup)

            self.verify_backup_checksum(
                backup,
                backup_path,
            )

            backup_root = self.get_backup_root()

            media_root = Path(settings.MEDIA_ROOT).resolve()

            backup_scope = backup.backup_scope

            safety_backup = None

            if backup_scope in [
                BackupLog.BackupScope.DATABASE,
                BackupLog.BackupScope.FULL,
            ]:

                database_path = self.get_database_path()

            # ------------------------------------------------
            # DATABASE RESTORE
            # ------------------------------------------------

            if backup_scope == BackupLog.BackupScope.DATABASE:

                self.validate_sqlite_database(backup_path)

                safety_backup = self.create_safety_backup(
                    database_path,
                    backup_root,
                )

                self.restore_sqlite_database(
                    backup_path,
                    database_path,
                )

                message = (
                    "Database restored successfully. "
                    "The previous database was backed up."
                )

            # ------------------------------------------------
            # MEDIA RESTORE
            # ------------------------------------------------

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

            # ------------------------------------------------
            # FULL RESTORE
            # ------------------------------------------------

            elif backup_scope == BackupLog.BackupScope.FULL:

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

                            destination_path = (
                                extracted_media.joinpath(*relative_path.parts)
                            ).resolve()

                            try:
                                destination_path.relative_to(extracted_media.resolve())
                            except ValueError:
                                raise ValueError("Unsafe media archive path.")

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

                    safety_backup = self.create_safety_backup(
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
                    "The previous database was backed up."
                )

            else:

                return Response(
                    {
                        "success": False,
                        "message": "Unsupported backup scope.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ------------------------------------------------
            # UPDATE RESTORE INFORMATION
            # ------------------------------------------------

            try:

                BackupLog.objects.filter(id=backup_id).update(
                    status=BackupLog.Status.RESTORED,
                    restored_at=timezone.now(),
                    restored_by=request.user,
                )

            except Exception:

                logger.exception("Could not update restored backup metadata.")

            self.record_audit_log(
                request=request,
                action="update",
                model_name="BackupLog",
                object_id=backup_id,
                description=(f"Restored {backup_scope} backup: " f"{backup.file_name}"),
            )

            return Response(
                {
                    "success": True,
                    "message": message,
                    "safety_backup": (str(safety_backup) if safety_backup else None),
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
# BACKUP SCHEDULE
# ============================================================


class BackupScheduleView(
    BackupHelperMixin,
    APIView,
):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner,
    ]

    def check_platform_owner(self, request):

        return request.user.is_superuser

    # ========================================================
    # GET GLOBAL SCHEDULE
    # ========================================================

    def get(self, request):

        if not self.check_platform_owner(request):
            return Response(
                {
                    "success": False,
                    "message": (
                        "Only the Platform Owner can manage "
                        "the global backup schedule."
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        schedule = BackupSchedule.objects.first()

        if not schedule:
            return Response(
                {
                    "success": False,
                    "message": ("Global backup schedule has not been configured."),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "success": True,
                "data": BackupScheduleSerializer(schedule).data,
            },
            status=status.HTTP_200_OK,
        )

    # ========================================================
    # CREATE / UPDATE GLOBAL SCHEDULE
    # ========================================================

    def post(self, request):

        if not self.check_platform_owner(request):
            return Response(
                {
                    "success": False,
                    "message": (
                        "Only the Platform Owner can configure " "automatic backups."
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        schedule = BackupSchedule.objects.first()

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

        backup_schedule = serializer.save(updated_by=request.user)

        self.record_audit_log(
            request=request,
            action=("update" if action == "updated" else "create"),
            model_name="BackupSchedule",
            object_id=backup_schedule.id,
            description=(
                f"Platform automatic backup schedule {action}. "
                f"Frequency: {backup_schedule.frequency}, "
                f"Scope: {backup_schedule.backup_scope}"
            ),
        )

        return Response(
            {
                "success": True,
                "message": (f"Global backup schedule {action} successfully."),
                "data": BackupScheduleSerializer(backup_schedule).data,
            },
            status=(
                status.HTTP_200_OK if action == "updated" else status.HTTP_201_CREATED
            ),
        )
