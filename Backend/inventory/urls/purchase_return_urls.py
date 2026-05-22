from django.urls import path

from inventory.views.purchase_return_views import (
    PurchaseReturnListCreateView,
    PurchaseReturnDetailView,
)

urlpatterns = [

    # ==========================================
    # PURCHASE RETURN LIST + CREATE
    # ==========================================

    path(
        "",
        PurchaseReturnListCreateView.as_view(),
        name="purchase-return-list-create",
    ),

    # ==========================================
    # PURCHASE RETURN DETAIL
    # ==========================================

    path(
        "<int:pk>/",
        PurchaseReturnDetailView.as_view(),
        name="purchase-return-detail",
    ),
]