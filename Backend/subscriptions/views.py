from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import (
    SubscriptionPlan,
    RetailerSubscription,
    PaymentHistory
)

from .serializers import (
    SubscriptionPlanSerializer,
    RetailerSubscriptionSerializer,
    RetailerSubscriptionCreateSerializer,
    PaymentHistorySerializer,
    PaymentHistoryCreateSerializer
)

from accounts.permissions import (
    IsPlatformOwner
)


# =====================================================
# SUBSCRIPTION PLAN
# =====================================================
class SubscriptionPlanListCreateView(generics.ListCreateAPIView):
    queryset = SubscriptionPlan.objects.all()

    serializer_class = SubscriptionPlanSerializer

    permission_classes = [
        IsAuthenticated,
        IsPlatformOwner
    ]


class SubscriptionPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubscriptionPlan.objects.all()

    serializer_class = SubscriptionPlanSerializer

    permission_classes = [
        IsAuthenticated,
        IsPlatformOwner
    ]


# =====================================================
# RETAILER SUBSCRIPTIONS
# =====================================================
class RetailerSubscriptionListView(generics.ListAPIView):

    queryset = RetailerSubscription.objects.select_related(
        "retailer",
        "plan"
    )

    serializer_class = RetailerSubscriptionSerializer

    permission_classes = [
        IsAuthenticated,
        IsPlatformOwner
    ]


class RetailerSubscriptionCreateView(generics.CreateAPIView):

    queryset = RetailerSubscription.objects.all()

    serializer_class = (
        RetailerSubscriptionCreateSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsPlatformOwner
    ]


class RetailerSubscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = RetailerSubscription.objects.select_related(
        "retailer",
        "plan"
    )

    serializer_class = (
        RetailerSubscriptionSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsPlatformOwner
    ]


# =====================================================
# PAYMENT HISTORY
# =====================================================
class PaymentHistoryListView(generics.ListAPIView):

    queryset = PaymentHistory.objects.select_related(
        "retailer",
        "subscription"
    )

    serializer_class = (
        PaymentHistorySerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsPlatformOwner
    ]


class PaymentHistoryCreateView(generics.CreateAPIView):

    queryset = PaymentHistory.objects.all()

    serializer_class = (
        PaymentHistoryCreateSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsPlatformOwner
    ]


class PaymentHistoryDetailView(generics.RetrieveAPIView):

    queryset = PaymentHistory.objects.select_related(
        "retailer",
        "subscription"
    )

    serializer_class = (
        PaymentHistorySerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsPlatformOwner
    ]