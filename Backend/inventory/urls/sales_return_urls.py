from django.urls import path

from inventory.views.sales_return_views import (
    SalesReturnListCreateView,
    SalesReturnDetailView,
)

urlpatterns = [

    # ==========================================
    # SALES RETURN LIST + CREATE
    # ==========================================

    path(
        "",
        SalesReturnListCreateView.as_view(),
        name="sales-return-list-create",
    ),

    # ==========================================
    # SALES RETURN DETAIL
    # ==========================================

    path(
        "<int:pk>/",
        SalesReturnDetailView.as_view(),
        name="sales-return-detail",
    ),
]