from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from masters.models import SalesOffer
from masters.serializers import SalesOfferSerializer

from accounts.permissions import IsAdmin, IsSuperAdmin
from subscriptions.utils import check_subscription_write_access
from accounts.views import create_audit_log

# =========================================================
# BASE QUERYSET HELPER
# =========================================================


def get_sales_offer_queryset(user, request):

    queryset = SalesOffer.objects.select_related(
        "product", "category", "manufacturer", "retailer", "branch"
    )

    # ================= PLATFORM OWNER =================

    if user.is_superuser:

        retailer_id = request.query_params.get("retailer")

        if retailer_id:

            queryset = queryset.filter(retailer_id=retailer_id)

        return queryset

    # ================= RETAILER USERS =================

    return queryset.filter(retailer=user.retailer)


# =========================================================
# CREATE
# =========================================================


class SalesOfferCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):

        user = request.user

        check_subscription_write_access(user.retailer)

        serializer = SalesOfferSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        sales_offer = serializer.save(retailer=user.retailer, branch=user.branch)

        create_audit_log(
            user=user,
            action="create",
            model_name="SalesOffer",
            object_id=sales_offer.id,
            description=(f"Created Sales Offer " f"{sales_offer.name}"),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Sales offer created successfully",
                "data": SalesOfferSerializer(sales_offer).data,
            },
            status=status.HTTP_201_CREATED,
        )


# =========================================================
# LIST
# =========================================================


class SalesOfferListAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        queryset = get_sales_offer_queryset(request.user, request)

        # =================================================
        # FILTER PARAMETERS
        # =================================================

        is_active = request.query_params.get("is_active")

        offer_type = request.query_params.get("offer_type")

        branch = request.query_params.get("branch")

        search = request.query_params.get("search")

        # =================================================
        # ACTIVE FILTER
        # =================================================

        if is_active is not None:

            queryset = queryset.filter(is_active=is_active.lower() == "true")

        # =================================================
        # OFFER TYPE FILTER
        # =================================================

        if offer_type:

            queryset = queryset.filter(offer_type=offer_type)

        # =================================================
        # BRANCH FILTER
        # =================================================

        if branch:

            queryset = queryset.filter(branch_id=branch)

        # =================================================
        # SEARCH
        # =================================================

        if search:

            queryset = queryset.filter(name__icontains=search)

        # =================================================
        # ORDER
        # =================================================

        queryset = queryset.order_by("-created_at")

        serializer = SalesOfferSerializer(queryset, many=True)

        return Response(
            {"success": True, "count": queryset.count(), "data": serializer.data},
            status=status.HTTP_200_OK,
        )


# =========================================================
# DETAIL
# =========================================================


class SalesOfferDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, request, pk):

        queryset = get_sales_offer_queryset(request.user, request)

        return queryset.filter(id=pk).first()

    def get(self, request, pk):

        offer = self.get_object(request, pk)

        if not offer:

            return Response(
                {"success": False, "message": "Sales offer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SalesOfferSerializer(offer)

        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE
# =========================================================


class SalesOfferUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, request, pk):

        queryset = get_sales_offer_queryset(request.user, request)

        return queryset.filter(id=pk).first()

    def put(self, request, pk):

        return self.update_offer(request, pk, partial=False)

    def patch(self, request, pk):

        return self.update_offer(request, pk, partial=True)

    def update_offer(self, request, pk, partial=False):

        offer = self.get_object(request, pk)

        if not offer:

            return Response(
                {"success": False, "message": "Sales offer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        check_subscription_write_access(request.user.retailer)

        old_name = offer.name

        serializer = SalesOfferSerializer(offer, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)

        offer = serializer.save()

        create_audit_log(
            user=request.user,
            action="update",
            model_name="SalesOffer",
            object_id=offer.id,
            description=(
                f"Updated Sales Offer " f"from {old_name} " f"to {offer.name}"
            ),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Sales offer updated successfully",
                "data": SalesOfferSerializer(offer).data,
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# SOFT DELETE / DEACTIVATE
# =========================================================


class SalesOfferSoftDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, request, pk):

        queryset = get_sales_offer_queryset(request.user, request)

        return queryset.filter(id=pk).first()

    def patch(self, request, pk):

        offer = self.get_object(request, pk)

        if not offer:

            return Response(
                {"success": False, "message": "Sales offer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not offer.is_active:

            return Response(
                {"success": False, "message": "Offer already inactive"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        check_subscription_write_access(request.user.retailer)

        offer.is_active = False

        offer.save(update_fields=["is_active"])

        create_audit_log(
            user=request.user,
            action="deactivate",
            model_name="SalesOffer",
            object_id=offer.id,
            description=(f"Deactivated Sales Offer " f"{offer.name}"),
            request=request,
        )

        return Response(
            {"success": True, "message": "Sales offer deactivated successfully"},
            status=status.HTTP_200_OK,
        )


# =========================================================
# ACTIVATE
# =========================================================


class SalesOfferActivateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, request, pk):

        queryset = get_sales_offer_queryset(request.user, request)

        return queryset.filter(id=pk).first()

    def patch(self, request, pk):

        offer = self.get_object(request, pk)

        if not offer:

            return Response(
                {"success": False, "message": "Sales offer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if offer.is_active:

            return Response(
                {"success": False, "message": "Offer already active"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        check_subscription_write_access(request.user.retailer)

        offer.is_active = True

        offer.save(update_fields=["is_active"])

        create_audit_log(
            user=request.user,
            action="activate",
            model_name="SalesOffer",
            object_id=offer.id,
            description=(f"Activated Sales Offer " f"{offer.name}"),
            request=request,
        )

        return Response(
            {"success": True, "message": "Sales offer activated successfully"},
            status=status.HTTP_200_OK,
        )


# =========================================================
# HARD DELETE
# =========================================================


class SalesOfferDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get_object(self, request, pk):

        queryset = get_sales_offer_queryset(request.user, request)

        return queryset.filter(id=pk).first()

    def delete(self, request, pk):

        offer = self.get_object(request, pk)

        if not offer:

            return Response(
                {"success": False, "message": "Sales offer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        check_subscription_write_access(request.user.retailer)

        offer_name = offer.name
        offer_id = offer.id

        offer.delete()

        create_audit_log(
            user=request.user,
            action="delete",
            model_name="SalesOffer",
            object_id=offer_id,
            description=(f"Deleted Sales Offer " f"{offer_name}"),
            request=request,
        )

        return Response(
            {"success": True, "message": "Sales offer deleted permanently"},
            status=status.HTTP_200_OK,
        )
