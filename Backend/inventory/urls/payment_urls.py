
from django.urls import path

from inventory.views.payment_views import (
    PaymentListCreateView,
    PaymentDetailView,
)


urlpatterns = [
    path("payments/",PaymentListCreateView.as_view(),name="payment-list-create",),
    path("payments/<int:pk>/",PaymentDetailView.as_view(),name="payment-detail",),
]
