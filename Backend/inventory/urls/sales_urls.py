from django.urls import path

from inventory.views.sales_views import (
    SalesListCreateView,
    SalesDetailView,
)

urlpatterns = [
    # SALES LIST + CREATE
    path("", SalesListCreateView.as_view(), name="sales-list-create",),
    # SALES DETAIL VIEW
    path("<int:pk>/", SalesDetailView.as_view(), name="sales-detail",),
]