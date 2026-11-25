from django.urls import path

from inventory.views.purchase_return_views import (
    PurchaseReturnListCreateView,
    PurchaseReturnDetailView,
)

urlpatterns = [
    path("purchase-returns/", PurchaseReturnListCreateView.as_view(),name="purchase-return-list-create",),
    path("purchase-returns/<int:pk>/",PurchaseReturnDetailView.as_view(),name="purchase-return-detail",),
]