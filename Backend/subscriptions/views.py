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

from accounts.permissions import IsPlatformOwner
from accounts.views import create_audit_log


# =====================================================
# SUBSCRIPTION PLAN
# =====================================================
class SubscriptionPlanListCreateView(generics.ListCreateAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        create_audit_log(
            user=request.user,
            action="view",
            model_name="SubscriptionPlan",
            object_id=None,
            description="Viewed Subscription Plans list",
            request=request
        )

        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        create_audit_log(
            user=request.user,
            action="create",
            model_name="SubscriptionPlan",
            object_id=response.data.get("id"),
            description="Created Subscription Plan",
            request=request
        )

        return response


class SubscriptionPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        create_audit_log(
            user=request.user,
            action="view",
            model_name="SubscriptionPlan",
            object_id=kwargs.get("pk"),
            description="Viewed Subscription Plan detail",
            request=request
        )

        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        create_audit_log(
            user=request.user,
            action="update",
            model_name="SubscriptionPlan",
            object_id=kwargs.get("pk"),
            description="Updated Subscription Plan",
            request=request
        )

        return response

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        response = super().destroy(request, *args, **kwargs)

        create_audit_log(
            user=request.user,
            action="delete",
            model_name="SubscriptionPlan",
            object_id=pk,
            description="Deleted Subscription Plan",
            request=request
        )

        return response


# =====================================================
# RETAILER SUBSCRIPTIONS
# =====================================================
class RetailerSubscriptionListView(generics.ListAPIView):
    queryset = RetailerSubscription.objects.select_related("retailer", "plan")
    serializer_class = RetailerSubscriptionSerializer
    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        create_audit_log(
            user=request.user,
            action="view",
            model_name="RetailerSubscription",
            object_id=None,
            description="Viewed Retailer Subscriptions list",
            request=request
        )

        return response


class RetailerSubscriptionCreateView(generics.CreateAPIView):
    queryset = RetailerSubscription.objects.all()
    serializer_class = RetailerSubscriptionCreateSerializer
    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        create_audit_log(
            user=request.user,
            action="create",
            model_name="RetailerSubscription",
            object_id=response.data.get("id"),
            description="Created Retailer Subscription",
            request=request
        )

        return response


class RetailerSubscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RetailerSubscription.objects.select_related("retailer", "plan")
    serializer_class = RetailerSubscriptionSerializer
    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        create_audit_log(
            user=request.user,
            action="view",
            model_name="RetailerSubscription",
            object_id=kwargs.get("pk"),
            description="Viewed Retailer Subscription detail",
            request=request
        )

        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        create_audit_log(
            user=request.user,
            action="update",
            model_name="RetailerSubscription",
            object_id=kwargs.get("pk"),
            description="Updated Retailer Subscription",
            request=request
        )

        return response

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        response = super().destroy(request, *args, **kwargs)

        create_audit_log(
            user=request.user,
            action="delete",
            model_name="RetailerSubscription",
            object_id=pk,
            description="Deleted Retailer Subscription",
            request=request
        )

        return response


# =====================================================
# PAYMENT HISTORY
# =====================================================
class PaymentHistoryListView(generics.ListAPIView):
    queryset = PaymentHistory.objects.select_related("retailer", "subscription")
    serializer_class = PaymentHistorySerializer
    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        create_audit_log(
            user=request.user,
            action="view",
            model_name="PaymentHistory",
            object_id=None,
            description="Viewed Payment History list",
            request=request
        )

        return response


class PaymentHistoryCreateView(generics.CreateAPIView):
    queryset = PaymentHistory.objects.all()
    serializer_class = PaymentHistoryCreateSerializer
    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        create_audit_log(
            user=request.user,
            action="create",
            model_name="PaymentHistory",
            object_id=response.data.get("id"),
            description="Created Payment History entry",
            request=request
        )

        return response


class PaymentHistoryDetailView(generics.RetrieveAPIView):
    queryset = PaymentHistory.objects.select_related("retailer", "subscription")
    serializer_class = PaymentHistorySerializer
    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        create_audit_log(
            user=request.user,
            action="view",
            model_name="PaymentHistory",
            object_id=kwargs.get("pk"),
            description="Viewed Payment History detail",
            request=request
        )

        return response