import logging

from celery import shared_task
from django.utils import timezone

from .models import BackupSchedule, BackupLog
from .views import BackupHelperMixin

logger = logging.getLogger(__name__)


@shared_task
def execute_scheduled_backup():

    now = timezone.localtime()

    schedule = BackupSchedule.objects.first()

    if not schedule or not schedule.is_active:
        return "Backup schedule is not active."

    if now.time() < schedule.backup_time:
        return "Backup time has not arrived."

    if schedule.frequency == BackupSchedule.Frequency.WEEKLY:
        if now.weekday() != 0:
            return "Today is not the scheduled backup day."

    elif schedule.frequency == BackupSchedule.Frequency.MONTHLY:
        if now.day != 1:
            return "Today is not the scheduled backup day."

    elif schedule.frequency != BackupSchedule.Frequency.DAILY:
        return "Unsupported backup frequency."

    if schedule.last_run_at:
        last_run_date = timezone.localtime(schedule.last_run_at).date()

        if last_run_date == now.date():
            return "Backup already executed today."

    try:

        backup = BackupHelperMixin().create_platform_backup(
            backup_scope=schedule.backup_scope,
            backup_type=BackupLog.BackupType.AUTOMATIC,
            created_by=None,
            notes="Automatically generated platform-level backup.",
        )

        schedule.last_run_at = timezone.now()

        schedule.save(
            update_fields=[
                "last_run_at",
                "updated_at",
            ]
        )

        logger.info(
            "Automatic backup completed successfully. Backup ID: %s",
            backup.id,
        )

        return f"Backup created successfully. ID: {backup.id}"

    except Exception:

        logger.exception("Automatic platform backup failed.")

        raise
