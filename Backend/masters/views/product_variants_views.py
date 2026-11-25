from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from masters.models.product_variants_models import ProductVariant
from masters.serializers.product_variants_serializers import ProductVariantSerializer

from accounts.permissions import IsAdminOrStaff
from subscriptions.utils import check_subscription_write_access


class ProductVariantBaseView:

    def is_platform_admin(self):
        user = self.request.user

        return user.is_superuser or getattr(user, "role", None) == "superadmin"

    def check_write_access(self):
        if self.is_platform_admin():
            return

        retailer = getattr(self.request.user, "retailer", None)

        if not retailer:
            raise PermissionDenied("Retailer account not found.")

        check_subscription_write_access(retailer)

    def get_queryset(self):
        queryset = ProductVariant.objects.select_related("product", "product__retailer")

        if self.is_platform_admin():
            return queryset

        retailer = getattr(self.request.user, "retailer", None)

        if not retailer:
            return queryset.none()

        return queryset.filter(product__retailer=retailer)

    def get_variant(self, pk):
        return get_object_or_404(self.get_queryset(), pk=pk)


class ProductVariantListCreateView(ProductVariantBaseView, APIView):

    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request):

        queryset = self.get_queryset().order_by("-id")

        serializer = ProductVariantSerializer(
            queryset, many=True, context={"request": request}
        )

        return Response(
            {
                "success": True,
                "message": "Product variants retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @transaction.atomic
    def post(self, request):

        self.check_write_access()

        serializer = ProductVariantSerializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Product variant created successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class ProductVariantDetailView(ProductVariantBaseView, APIView):

    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request, pk):

        variant = self.get_variant(pk)

        serializer = ProductVariantSerializer(variant, context={"request": request})

        return Response(
            {
                "success": True,
                "message": "Product variant retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @transaction.atomic
    def put(self, request, pk):

        self.check_write_access()

        variant = self.get_variant(pk)

        serializer = ProductVariantSerializer(
            variant, data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Product variant updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @transaction.atomic
    def patch(self, request, pk):

        self.check_write_access()

        variant = self.get_variant(pk)

        serializer = ProductVariantSerializer(
            variant, data=request.data, partial=True, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Product variant updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @transaction.atomic
    def delete(self, request, pk):

        self.check_write_access()

        variant = self.get_variant(pk)

        variant.is_active = False
        variant.save(update_fields=["is_active", "updated_at"])

        return Response(
            {
                "success": True,
                "message": "Product variant deactivated successfully.",
                "data": None,
            },
            status=status.HTTP_200_OK,
        )
