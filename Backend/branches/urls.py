from django.urls import path
from .views import *

urlpatterns = [
    path('branches/create/', BranchCreateView.as_view()),
    path('branches/', BranchListView.as_view()),
    path('branches/<int:pk>/', BranchDetailView.as_view()),
    path('branches/update/<int:pk>/', BranchUpdateView.as_view()),
    path('branches/deactivate/<int:pk>/', BranchSoftDeleteView.as_view()),
    path('branches/restore/<int:pk>/', BranchRestoreView.as_view()),
    path('branches/delete/<int:pk>/', BranchHardDeleteView.as_view()),
    path('branches/filter/', BranchStatusFilterView.as_view()),
]
