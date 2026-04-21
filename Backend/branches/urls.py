from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', BranchCreateView.as_view()),
    path('', BranchListView.as_view()),
    path('<int:pk>/', BranchDetailView.as_view()),
    path('update/<int:pk>/', BranchUpdateView.as_view()),
    path('deactivate/<int:pk>/', BranchSoftDeleteView.as_view()),
    path('restore/<int:pk>/', BranchRestoreView.as_view()),
    path('delete/<int:pk>/', BranchHardDeleteView.as_view()),
    path('filter/', BranchStatusFilterView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)