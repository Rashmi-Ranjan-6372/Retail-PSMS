from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import SubscriptionPlan, RetailerSubscription, PaymentHistory

from .serializers import (
    SubscriptionPlanSerializer,
    RetailerSubscriptionSerializer,
    RetailerSubscriptionCreateSerializer,
    PaymentHistorySerializer,
    PaymentHistoryCreateSerializer,
)

from accounts.permissions import IsPlatformOwner
from accounts.views import create_audit_log

# =====================================================
# SUBSCRIPTION PLAN LIST / CREATE
# =====================================================


class SubscriptionPlanListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def get(self, request):

        plans = SubscriptionPlan.objects.all()

        serializer = SubscriptionPlanSerializer(plans, many=True)

        create_audit_log(
            user=request.user,
            action="view",
            model_name="SubscriptionPlan",
            object_id=None,
            description="Viewed Subscription Plans list",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Subscription Plans retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):

        serializer = SubscriptionPlanSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        plan = serializer.save()

        create_audit_log(
            user=request.user,
            action="create",
            model_name="SubscriptionPlan",
            object_id=plan.id,
            description="Created Subscription Plan",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Subscription Plan created successfully.",
                "data": SubscriptionPlanSerializer(plan).data,
            },
            status=status.HTTP_201_CREATED,
        )


# =====================================================
# SUBSCRIPTION PLAN DETAIL
# =====================================================


class SubscriptionPlanDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def get_object(self, pk):

        return SubscriptionPlan.objects.filter(id=pk).first()

    def get(self, request, pk):

        plan = self.get_object(pk)

        if not plan:
            return Response(
                {
                    "success": False,
                    "message": "Subscription Plan not found.",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SubscriptionPlanSerializer(plan)

        create_audit_log(
            user=request.user,
            action="view",
            model_name="SubscriptionPlan",
            object_id=pk,
            description="Viewed Subscription Plan detail",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Subscription Plan retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):

        plan = self.get_object(pk)

        if not plan:
            return Response(
                {
                    "success": False,
                    "message": "Subscription Plan not found.",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SubscriptionPlanSerializer(plan, data=request.data)

        serializer.is_valid(raise_exception=True)

        plan = serializer.save()

        create_audit_log(
            user=request.user,
            action="update",
            model_name="SubscriptionPlan",
            object_id=pk,
            description="Updated Subscription Plan",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Subscription Plan updated successfully.",
                "data": SubscriptionPlanSerializer(plan).data,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk):

        plan = self.get_object(pk)

        if not plan:
            return Response(
                {
                    "success": False,
                    "message": "Subscription Plan not found.",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SubscriptionPlanSerializer(plan, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        plan = serializer.save()

        create_audit_log(
            user=request.user,
            action="update",
            model_name="SubscriptionPlan",
            object_id=pk,
            description="Updated Subscription Plan",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Subscription Plan updated successfully.",
                "data": SubscriptionPlanSerializer(plan).data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):

        plan = self.get_object(pk)

        if not plan:
            return Response(
                {
                    "success": False,
                    "message": "Subscription Plan not found.",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        plan.delete()

        create_audit_log(
            user=request.user,
            action="delete",
            model_name="SubscriptionPlan",
            object_id=pk,
            description="Deleted Subscription Plan",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Subscription Plan deleted successfully.",
                "data": None,
            },
            status=status.HTTP_200_OK,
        )


# =====================================================
# RETAILER SUBSCRIPTION LIST
# =====================================================


class RetailerSubscriptionListAPIView(APIView):

    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def get(self, request):

        subscriptions = RetailerSubscription.objects.select_related("retailer", "plan")

        serializer = RetailerSubscriptionSerializer(subscriptions, many=True)

        create_audit_log(
            user=request.user,
            action="view",
            model_name="RetailerSubscription",
            object_id=None,
            description="Viewed Retailer Subscriptions list",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Retailer Subscriptions retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# =====================================================
# RETAILER SUBSCRIPTION CREATE
# =====================================================


class RetailerSubscriptionCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def post(self, request):

        serializer = RetailerSubscriptionCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        subscription = serializer.save()

        create_audit_log(
            user=request.user,
            action="create",
            model_name="RetailerSubscription",
            object_id=subscription.id,
            description="Created Retailer Subscription",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Retailer Subscription created successfully.",
                "data": RetailerSubscriptionSerializer(subscription).data,
            },
            status=status.HTTP_201_CREATED,
        )


# =====================================================
# RETAILER SUBSCRIPTION DETAIL
# =====================================================


class RetailerSubscriptionDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def get_object(self, pk):

        return (
            RetailerSubscription.objects.select_related("retailer", "plan")
            .filter(id=pk)
            .first()
        )

    def get(self, request, pk):

        subscription = self.get_object(pk)

        if not subscription:
            return Response(
                {
                    "success": False,
                    "message": "Retailer Subscription not found.",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RetailerSubscriptionSerializer(subscription)

        create_audit_log(
            user=request.user,
            action="view",
            model_name="RetailerSubscription",
            object_id=pk,
            description="Viewed Retailer Subscription detail",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Retailer Subscription retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):

        subscription = self.get_object(pk)

        if not subscription:
            return Response(
                {
                    "success": False,
                    "message": "Retailer Subscription not found.",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RetailerSubscriptionSerializer(subscription, data=request.data)

        serializer.is_valid(raise_exception=True)

        subscription = serializer.save()

        create_audit_log(
            user=request.user,
            action="update",
            model_name="RetailerSubscription",
            object_id=pk,
            description="Updated Retailer Subscription",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Retailer Subscription updated successfully.",
                "data": RetailerSubscriptionSerializer(subscription).data,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk):

        subscription = self.get_object(pk)

        if not subscription:
            return Response(
                {
                    "success": False,
                    "message": "Retailer Subscription not found.",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RetailerSubscriptionSerializer(
            subscription, data=request.data, partial=True
        )

        serializer.is_valid(raise_exception=True)

        subscription = serializer.save()

        create_audit_log(
            user=request.user,
            action="update",
            model_name="RetailerSubscription",
            object_id=pk,
            description="Updated Retailer Subscription",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Retailer Subscription updated successfully.",
                "data": RetailerSubscriptionSerializer(subscription).data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):

        subscription = self.get_object(pk)

        if not subscription:
            return Response(
                {
                    "success": False,
                    "message": "Retailer Subscription not found.",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        subscription.delete()

        create_audit_log(
            user=request.user,
            action="delete",
            model_name="RetailerSubscription",
            object_id=pk,
            description="Deleted Retailer Subscription",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Retailer Subscription deleted successfully.",
                "data": None,
            },
            status=status.HTTP_200_OK,
        )


# =====================================================
# PAYMENT HISTORY LIST
# =====================================================


class PaymentHistoryListAPIView(APIView):

    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def get(self, request):

        payments = PaymentHistory.objects.select_related("retailer", "subscription")

        serializer = PaymentHistorySerializer(payments, many=True)

        create_audit_log(
            user=request.user,
            action="view",
            model_name="PaymentHistory",
            object_id=None,
            description="Viewed Payment History list",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Payment History retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# =====================================================
# PAYMENT HISTORY CREATE
# =====================================================


class PaymentHistoryCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def post(self, request):

        serializer = PaymentHistoryCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        payment = serializer.save()

        create_audit_log(
            user=request.user,
            action="create",
            model_name="PaymentHistory",
            object_id=payment.id,
            description="Created Payment History entry",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Payment History created successfully.",
                "data": PaymentHistorySerializer(payment).data,
            },
            status=status.HTTP_201_CREATED,
        )


# =====================================================
# PAYMENT HISTORY DETAIL
# =====================================================


class PaymentHistoryDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsPlatformOwner]

    def get_object(self, pk):

        return (
            PaymentHistory.objects.select_related("retailer", "subscription")
            .filter(id=pk)
            .first()
        )

    def get(self, request, pk):

        payment = self.get_object(pk)

        if not payment:
            return Response(
                {
                    "success": False,
                    "message": "Payment History not found.",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PaymentHistorySerializer(payment)

        create_audit_log(
            user=request.user,
            action="view",
            model_name="PaymentHistory",
            object_id=pk,
            description="Viewed Payment History detail",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Payment History retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
