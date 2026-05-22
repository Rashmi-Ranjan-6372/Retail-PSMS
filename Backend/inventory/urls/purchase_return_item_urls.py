from django.urls import path

from inventory.views.purchase_return_item_views import (
    PurchaseReturnItemListCreateView,
    PurchaseReturnItemDetailView,
)

urlpatterns = [

    path(
        "",
        PurchaseReturnItemListCreateView.as_view(),
        name="purchase-return-item-list-create",
    ),

    path(
        "<int:pk>/",
        PurchaseReturnItemDetailView.as_view(),
        name="purchase-return-item-detail",
    ),
]