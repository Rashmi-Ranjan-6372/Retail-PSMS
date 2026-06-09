from django.urls import path

from .views import (
    SubscriptionPlanListCreateView,
    SubscriptionPlanDetailView,
    RetailerSubscriptionListView,
    RetailerSubscriptionCreateView,
    RetailerSubscriptionDetailView,
    PaymentHistoryListView,
    PaymentHistoryCreateView,
    PaymentHistoryDetailView,
)

urlpatterns = [
    # =====================================================
    # PLANS
    # =====================================================
    path("plans/", SubscriptionPlanListCreateView.as_view(), name="subscription-plan-list-create"),
    path("plans/<int:pk>/", SubscriptionPlanDetailView.as_view(), name="subscription-plan-detail"),

    # =====================================================
    # RETAILER SUBSCRIPTIONS
    # =====================================================
    path("retailer-subscriptions/", RetailerSubscriptionListView.as_view(), name="retailer-subscription-list"),
    path("retailer-subscriptions/create/", RetailerSubscriptionCreateView.as_view(), name="retailer-subscription-create"),
    path("retailer-subscriptions/<int:pk>/", RetailerSubscriptionDetailView.as_view(), name="retailer-subscription-detail"),

    # =====================================================
    # PAYMENTS
    # =====================================================
    path("payments/", PaymentHistoryListView.as_view(), name="payment-history-list"),
    path("payments/create/", PaymentHistoryCreateView.as_view(), name="payment-history-create"),
    path("payments/<int:pk>/", PaymentHistoryDetailView.as_view(), name="payment-history-detail"),
]