
from django.urls import path

from masters.views.suppliers_views import (
    SupplierCreateAPIView,
    SupplierListAPIView,
    SupplierDetailAPIView,
    SupplierUpdateAPIView,
    SupplierSoftDeleteAPIView,
    SupplierActivateAPIView,
    SupplierDeleteAPIView,
)

urlpatterns = [
    path("suppliers/", SupplierListAPIView.as_view(), name="supplier-list"),
    path("suppliers/create/", SupplierCreateAPIView.as_view(), name="supplier-create"),
    path("suppliers/update/<int:pk>/", SupplierUpdateAPIView.as_view(), name="supplier-update"),
    path("suppliers/deactivate/<int:pk>/", SupplierSoftDeleteAPIView.as_view(), name="supplier-deactivate"),
    path("suppliers/activate/<int:pk>/", SupplierActivateAPIView.as_view(), name="supplier-activate"),
    path("suppliers/delete/<int:pk>/", SupplierDeleteAPIView.as_view(), name="supplier-delete"),
    path("suppliers/<int:pk>/", SupplierDetailAPIView.as_view(), name="supplier-detail"),
]
