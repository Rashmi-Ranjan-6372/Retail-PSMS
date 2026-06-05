from django.urls import path
from .views import (
    CreateBackupView,
    BackupHistoryView,
    BackupDetailView,
    RestoreBackupView,
)

urlpatterns = [
    path("create/", CreateBackupView.as_view()),
    path("history/", BackupHistoryView.as_view()),
    path("<int:pk>/", BackupDetailView.as_view()),
    path("restore/", RestoreBackupView.as_view()),
]