from django.urls import path
from masters.views.suppliers_views import *
urlpatterns = [
    path('', SupplierListView.as_view()),
    path('create/', SupplierCreateView.as_view()),
    path('<int:pk>/', SupplierDetailView.as_view()),
    path('<int:pk>/update/', SupplierUpdateView.as_view()),
    path('<int:pk>/deactivate/', SupplierSoftDeleteView.as_view()),
    path('<int:pk>/delete/', SupplierDeleteView.as_view()),
]