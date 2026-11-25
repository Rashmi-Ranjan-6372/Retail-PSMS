from django.urls import path

from inventory.views.sales_return_item_views import (
    SalesReturnItemListCreateView,
    SalesReturnItemDetailView,
)

urlpatterns = [
    path("sales-return-items/",SalesReturnItemListCreateView.as_view(),name="sales-return-item-list-create",),
    path("sales-return-items/<int:pk>/",SalesReturnItemDetailView.as_view(),name="sales-return-item-detail",),
]