from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    BranchCreateView,
    BranchListView,
    BranchDetailView,
    BranchUpdateView,
    BranchSoftDeleteView,
    BranchRestoreView,
    BranchHardDeleteView,
    BranchStatusFilterView,
)

urlpatterns = [
    path("create/", BranchCreateView.as_view(), name="branch-create"),
    path("", BranchListView.as_view(), name="branch-list"),
    path("filter/", BranchStatusFilterView.as_view(), name="branch-filter"),
    path("update/<int:pk>/", BranchUpdateView.as_view(), name="branch-update"),
    path("deactivate/<int:pk>/", BranchSoftDeleteView.as_view(), name="branch-deactivate"),
    path("restore/<int:pk>/", BranchRestoreView.as_view(), name="branch-restore"),
    path("delete/<int:pk>/", BranchHardDeleteView.as_view(), name="branch-delete"),
    path("<int:pk>/", BranchDetailView.as_view(), name="branch-detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)