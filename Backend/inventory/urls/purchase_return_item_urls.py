from django.urls import path

from inventory.views.purchase_return_item_views import (
    PurchaseReturnItemListCreateView,
    PurchaseReturnItemDetailView,
)

urlpatterns = [

    path("purchase-return-items/",PurchaseReturnItemListCreateView.as_view(),name="purchase-return-item-list-create",),
    path("purchase-return-items/<int:pk>/",PurchaseReturnItemDetailView.as_view(),name="purchase-return-item-detail",),
]