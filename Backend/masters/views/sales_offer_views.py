from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from masters.models import SalesOffer
from masters.serializers import SalesOfferSerializer
from accounts.permissions import IsAdmin, IsSuperAdmin


# =========================================================
# BASE RETAILER MIXIN
# =========================================================

class RetailerSalesOfferMixin:

    def get_queryset(self):

        user = self.request.user

        queryset = SalesOffer.objects.select_related(
            "product",
            "category",
            "manufacturer",
            "retailer",
            "branch"
        )

        # ================= PLATFORM OWNER =================
        if user.is_superuser:

            retailer_id = self.request.query_params.get("retailer")

            if retailer_id:
                queryset = queryset.filter(
                    retailer_id=retailer_id
                )

            return queryset

        # ================= RETAILER USERS =================
        return queryset.filter(
            retailer=user.retailer
        )


# =========================================================
# CREATE
# =========================================================

class SalesOfferCreateView(
    RetailerSalesOfferMixin,
    generics.CreateAPIView
):

    serializer_class = SalesOfferSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def perform_create(self, serializer):

        user = self.request.user

        serializer.save(
            retailer=user.retailer,
            branch=user.branch
        )

    def create(self, request, *args, **kwargs):

        response = super().create(request, *args, **kwargs)

        return Response({
            "success": True,
            "message": "Sales offer created successfully",
            "data": response.data
        }, status=status.HTTP_201_CREATED)


# =========================================================
# LIST
# =========================================================

class SalesOfferListView(
    RetailerSalesOfferMixin,
    generics.ListAPIView
):

    serializer_class = SalesOfferSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        is_active = self.request.query_params.get(
            "is_active"
        )

        offer_type = self.request.query_params.get(
            "offer_type"
        )

        branch = self.request.query_params.get(
            "branch"
        )

        search = self.request.query_params.get(
            "search"
        )

        # ================= FILTERS =================

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        if offer_type:
            queryset = queryset.filter(
                offer_type=offer_type
            )

        if branch:
            queryset = queryset.filter(
                branch_id=branch
            )

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        return queryset.order_by("-created_at")

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        })


# =========================================================
# DETAIL
# =========================================================

class SalesOfferDetailView(
    RetailerSalesOfferMixin,
    generics.RetrieveAPIView
):

    serializer_class = SalesOfferSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):
        return super().get_queryset()


# =========================================================
# UPDATE
# =========================================================

class SalesOfferUpdateView(
    RetailerSalesOfferMixin,
    generics.UpdateAPIView
):

    serializer_class = SalesOfferSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):
        return super().get_queryset()

    def update(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({
            "success": True,
            "message": "Sales offer updated successfully",
            "data": serializer.data
        })


# =========================================================
# SOFT DELETE
# =========================================================

class SalesOfferSoftDeleteView(
    RetailerSalesOfferMixin,
    generics.UpdateAPIView
):

    serializer_class = SalesOfferSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):
        return super().get_queryset()

    def patch(self, request, *args, **kwargs):

        offer = self.get_object()

        if not offer.is_active:
            return Response({
                "success": False,
                "message": "Offer already inactive"
            }, status=status.HTTP_400_BAD_REQUEST)

        offer.is_active = False

        offer.save(update_fields=["is_active"])

        return Response({
            "success": True,
            "message": "Sales offer deactivated successfully"
        })


# =========================================================
# ACTIVATE
# =========================================================

class SalesOfferActivateView(
    RetailerSalesOfferMixin,
    generics.UpdateAPIView
):

    serializer_class = SalesOfferSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):
        return super().get_queryset()

    def patch(self, request, *args, **kwargs):

        offer = self.get_object()

        if offer.is_active:
            return Response({
                "success": False,
                "message": "Offer already active"
            }, status=status.HTTP_400_BAD_REQUEST)

        offer.is_active = True

        offer.save(update_fields=["is_active"])

        return Response({
            "success": True,
            "message": "Sales offer activated successfully"
        })


# =========================================================
# HARD DELETE
# =========================================================

class SalesOfferDeleteView(
    RetailerSalesOfferMixin,
    generics.DestroyAPIView
):

    serializer_class = SalesOfferSerializer

    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin
    ]

    def get_queryset(self):
        return super().get_queryset()

    def destroy(self, request, *args, **kwargs):

        offer = self.get_object()

        offer.delete()

        return Response({
            "success": True,
            "message": "Sales offer deleted permanently"
        }, status=status.HTTP_200_OK)