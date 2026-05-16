from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from masters.models import Product
from masters.serializers import ProductSerializer

from accounts.permissions import IsAdmin, IsSuperAdmin


# =========================================================
# BASE QUERYSET MIXIN
# =========================================================

class RetailerProductMixin:

    def get_queryset(self):

        user = self.request.user

        queryset = Product.objects.select_related(
            "category",
            "manufacturer",
            "retailer",
            "branch"
        )

        # ================= PLATFORM OWNER =================
        if user.is_superuser:

            retailer_id = self.request.query_params.get("retailer")

            if retailer_id:
                queryset = queryset.filter(retailer_id=retailer_id)

            return queryset

        # ================= RETAILER USERS =================
        return queryset.filter(
            retailer=user.retailer
        )


# =========================================================
# CREATE
# =========================================================

class ProductCreateView(
    RetailerProductMixin,
    generics.CreateAPIView
):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

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
            "message": "Product created successfully",
            "data": response.data
        }, status=status.HTTP_201_CREATED)


# =========================================================
# LIST
# =========================================================

class ProductListView(
    RetailerProductMixin,
    generics.ListAPIView
):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):

        queryset = super().get_queryset()

        is_active = self.request.query_params.get("is_active")
        category = self.request.query_params.get("category")
        manufacturer = self.request.query_params.get("manufacturer")
        search = self.request.query_params.get("search")
        prescription_required = self.request.query_params.get(
            "prescription_required"
        )
        branch = self.request.query_params.get("branch")

        # ================= FILTERS =================

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        if category:
            queryset = queryset.filter(
                category_id=category
            )

        if manufacturer:
            queryset = queryset.filter(
                manufacturer_id=manufacturer
            )

        if prescription_required is not None:
            queryset = queryset.filter(
                prescription_required=
                prescription_required.lower() == "true"
            )

        if branch:
            queryset = queryset.filter(
                branch_id=branch
            )

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        return queryset.order_by("name")

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

class ProductDetailView(
    RetailerProductMixin,
    generics.RetrieveAPIView
):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return super().get_queryset()


# =========================================================
# UPDATE
# =========================================================

class ProductUpdateView(
    RetailerProductMixin,
    generics.UpdateAPIView
):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

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
            "message": "Product updated successfully",
            "data": serializer.data
        })


# =========================================================
# SOFT DELETE
# =========================================================

class ProductSoftDeleteView(
    RetailerProductMixin,
    generics.UpdateAPIView
):

    serializer_class = ProductSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):
        return super().get_queryset()

    def patch(self, request, *args, **kwargs):

        product = self.get_object()

        if not product.is_active:
            return Response({
                "success": False,
                "message": "Product already inactive"
            }, status=status.HTTP_400_BAD_REQUEST)

        product.is_active = False

        product.save(update_fields=["is_active"])

        return Response({
            "success": True,
            "message": "Product deactivated successfully"
        })


# =========================================================
# ACTIVATE PRODUCT
# =========================================================

class ProductActivateView(
    RetailerProductMixin,
    generics.UpdateAPIView
):

    serializer_class = ProductSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):
        return super().get_queryset()

    def patch(self, request, *args, **kwargs):

        product = self.get_object()

        if product.is_active:
            return Response({
                "success": False,
                "message": "Product already active"
            }, status=status.HTTP_400_BAD_REQUEST)

        product.is_active = True

        product.save(update_fields=["is_active"])

        return Response({
            "success": True,
            "message": "Product activated successfully"
        })


# =========================================================
# HARD DELETE
# =========================================================

class ProductDeleteView(
    RetailerProductMixin,
    generics.DestroyAPIView
):

    serializer_class = ProductSerializer

    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin
    ]

    def get_queryset(self):
        return super().get_queryset()

    def destroy(self, request, *args, **kwargs):

        product = self.get_object()

        product.delete()

        return Response({
            "success": True,
            "message": "Product deleted permanently"
        }, status=status.HTTP_200_OK)