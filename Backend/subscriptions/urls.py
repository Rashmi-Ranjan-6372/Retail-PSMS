from django.urls import path

from .views import (
    SubscriptionPlanListCreateAPIView,
    SubscriptionPlanDetailAPIView,
    RetailerSubscriptionListAPIView,
    RetailerSubscriptionCreateAPIView,
    RetailerSubscriptionDetailAPIView,
    PaymentHistoryListAPIView,
    PaymentHistoryCreateAPIView,
    PaymentHistoryDetailAPIView,
)

urlpatterns = [
    # =====================================================
    # PLANS
    # =====================================================
    path("plans/", SubscriptionPlanListCreateAPIView.as_view(), name="subscription-plan-list-create"),
    path("plans/<int:pk>/", SubscriptionPlanDetailAPIView.as_view(), name="subscription-plan-detail"),

    # =====================================================
    # RETAILER SUBSCRIPTIONS
    # =====================================================
    path("retailer-subscriptions/", RetailerSubscriptionListAPIView.as_view(), name="retailer-subscription-list"),
    path("retailer-subscriptions/create/", RetailerSubscriptionCreateAPIView.as_view(), name="retailer-subscription-create"),
    path("retailer-subscriptions/<int:pk>/", RetailerSubscriptionDetailAPIView.as_view(), name="retailer-subscription-detail"),

    # =====================================================
    # PAYMENTS
    # =====================================================
    path("payments/", PaymentHistoryListAPIView.as_view(), name="payment-history-list"),
    path("payments/create/", PaymentHistoryCreateAPIView.as_view(), name="payment-history-create"),
    path("payments/<int:pk>/", PaymentHistoryDetailAPIView.as_view(), name="payment-history-detail"),
]