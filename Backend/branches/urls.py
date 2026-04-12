from django.urls import path
from .views import (
    BranchCreateView,
    BranchListView,
    BranchDetailView,
    BranchUpdateView,
    BranchDeleteView
)

urlpatterns = [
    path('', BranchListView.as_view(), name='branch-list'),
    path('create/', BranchCreateView.as_view(), name='branch-create'),
    path('<int:pk>/', BranchDetailView.as_view(), name='branch-detail'),
    path('<int:pk>/update/', BranchUpdateView.as_view(), name='branch-update'),
    path('<int:pk>/delete/', BranchDeleteView.as_view(), name='branch-delete'),
]