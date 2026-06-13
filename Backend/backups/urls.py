from django.urls import path
from .views import (
    CreateBackupView,
    BackupHistoryView,
    BackupDetailView,
    DownloadBackupView,
    RestoreBackupView,
    BackupScheduleView,
)

urlpatterns = [
    path("create/", CreateBackupView.as_view()),
    path("history/", BackupHistoryView.as_view()),
    path("<int:pk>/", BackupDetailView.as_view()),
    path("download/<int:pk>/", DownloadBackupView.as_view()),
    path("restore/", RestoreBackupView.as_view()),
    path("schedule/", BackupScheduleView.as_view()),
]