from django.urls import path

from inventory.views.sales_return_item_views import (
    SalesReturnItemListCreateView,
    SalesReturnItemDetailView,
)

urlpatterns = [

    path(
        "",
        SalesReturnItemListCreateView.as_view(),
        name="sales-return-item-list-create",
    ),

    path(
        "<int:pk>/",
        SalesReturnItemDetailView.as_view(),
        name="sales-return-item-detail",
    ),
]