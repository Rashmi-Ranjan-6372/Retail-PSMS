from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from masters.models import SalesOffer
from masters.serializers import SalesOfferSerializer

from accounts.permissions import IsAdmin, IsSuperAdmin


# ================= CREATE ================= #
class SalesOfferCreateView(generics.CreateAPIView):
    serializer_class = SalesOfferSerializer
    permission_classes = [IsAuthenticated,IsAdmin]

# ================= LIST ================= #
class SalesOfferListView(generics.ListAPIView):
    serializer_class = SalesOfferSerializer
    permission_classes = [IsAuthenticated,IsAdmin]

    def get_queryset(self):
        queryset = SalesOffer.objects.select_related(
            "product",
            "category",
            "manufacturer"
        ).all()

        is_active = self.request.query_params.get("is_active")
        offer_type = self.request.query_params.get("offer_type")
        search = self.request.query_params.get("search")

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        if offer_type:
            queryset = queryset.filter(
                offer_type=offer_type
            )

        # Search
        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        return queryset.order_by("-created_at")

# ================= DETAIL ================= #
class SalesOfferDetailView(generics.RetrieveAPIView):
    serializer_class = SalesOfferSerializer
    permission_classes = [IsAuthenticated,IsAdmin]
    queryset = SalesOffer.objects.select_related(
        "product",
        "category",
        "manufacturer"
    ).all()

# ================= UPDATE ================= #
class SalesOfferUpdateView(generics.UpdateAPIView):
    serializer_class = SalesOfferSerializer
    permission_classes = [IsAuthenticated,IsAdmin]
    queryset = SalesOffer.objects.all()

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


# ================= SOFT DELETE ================= #

class SalesOfferSoftDeleteView(generics.UpdateAPIView):

    serializer_class = SalesOfferSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    queryset = SalesOffer.objects.all()

    def patch(self, request, *args, **kwargs):

        offer = self.get_object()

        if not offer.is_active:
            return Response({
                "success": False,
                "message": "Offer already inactive"
            }, status=400)

        offer.is_active = False

        offer.save()

        return Response({
            "success": True,
            "message": "Sales offer deactivated successfully"
        })


# ================= HARD DELETE ================= #

class SalesOfferDeleteView(generics.DestroyAPIView):

    serializer_class = SalesOfferSerializer

    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin
    ]

    queryset = SalesOffer.objects.all()

    def destroy(self, request, *args, **kwargs):

        offer = self.get_object()

        offer.delete()

        return Response({
            "success": True,
            "message": "Sales offer deleted permanently"
        }, status=status.HTTP_200_OK)