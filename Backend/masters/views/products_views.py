from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from masters.models import Product
from masters.serializers import ProductSerializer

from accounts.permissions import IsAdmin, IsSuperAdmin
from subscriptions.utils import check_subscription_write_access
from accounts.views import create_audit_log

# =========================================================
# BASE QUERYSET HELPER
# =========================================================


def get_product_queryset(user, request):

    queryset = Product.objects.select_related(
        "category", "manufacturer", "retailer", "branch"
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
# PRODUCT CREATE
# =========================================================


class ProductCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):

        user = request.user

        check_subscription_write_access(user.retailer)

        serializer = ProductSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        product = serializer.save(retailer=user.retailer, branch=user.branch)

        create_audit_log(
            user=user,
            action="create",
            model_name="Product",
            object_id=product.id,
            description=f"Created Product {product.name}",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Product created successfully",
                "data": ProductSerializer(product).data,
            },
            status=status.HTTP_201_CREATED,
        )


# =========================================================
# PRODUCT LIST
# =========================================================


class ProductListAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        queryset = get_product_queryset(request.user, request)

        # =================================================
        # FILTER PARAMETERS
        # =================================================

        is_active = request.query_params.get("is_active")

        category = request.query_params.get("category")

        manufacturer = request.query_params.get("manufacturer")

        search = request.query_params.get("search")

        prescription_required = request.query_params.get("prescription_required")

        branch = request.query_params.get("branch")

        # =================================================
        # ACTIVE FILTER
        # =================================================

        if is_active is not None:

            queryset = queryset.filter(is_active=is_active.lower() == "true")

        # =================================================
        # CATEGORY FILTER
        # =================================================

        if category:

            queryset = queryset.filter(category_id=category)

        # =================================================
        # MANUFACTURER FILTER
        # =================================================

        if manufacturer:

            queryset = queryset.filter(manufacturer_id=manufacturer)

        # =================================================
        # PRESCRIPTION FILTER
        # =================================================

        if prescription_required is not None:

            queryset = queryset.filter(
                prescription_required=(prescription_required.lower() == "true")
            )

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

        queryset = queryset.order_by("name")

        serializer = ProductSerializer(queryset, many=True)

        return Response(
            {"success": True, "count": queryset.count(), "data": serializer.data},
            status=status.HTTP_200_OK,
        )


# =========================================================
# PRODUCT DETAIL
# =========================================================


class ProductDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, request, pk):

        queryset = get_product_queryset(request.user, request)

        return queryset.filter(id=pk).first()

    def get(self, request, pk):

        product = self.get_object(request, pk)

        if not product:

            return Response(
                {"success": False, "message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProductSerializer(product)

        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


# =========================================================
# PRODUCT UPDATE
# =========================================================


class ProductUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, request, pk):

        queryset = get_product_queryset(request.user, request)

        return queryset.filter(id=pk).first()

    def put(self, request, pk):

        return self.update_product(request, pk, partial=False)

    def patch(self, request, pk):

        return self.update_product(request, pk, partial=True)

    def update_product(self, request, pk, partial=False):

        product = self.get_object(request, pk)

        if not product:

            return Response(
                {"success": False, "message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        check_subscription_write_access(request.user.retailer)

        old_name = product.name

        serializer = ProductSerializer(product, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)

        product = serializer.save()

        create_audit_log(
            user=request.user,
            action="update",
            model_name="Product",
            object_id=product.id,
            description=(f"Updated Product from " f"{old_name} to {product.name}"),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Product updated successfully",
                "data": ProductSerializer(product).data,
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# PRODUCT SOFT DELETE
# =========================================================


class ProductSoftDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, request, pk):

        queryset = get_product_queryset(request.user, request)

        return queryset.filter(id=pk).first()

    def patch(self, request, pk):

        product = self.get_object(request, pk)

        if not product:

            return Response(
                {"success": False, "message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        check_subscription_write_access(request.user.retailer)

        if not product.is_active:

            return Response(
                {"success": False, "message": "Product already inactive"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product.is_active = False

        product.save(update_fields=["is_active"])

        create_audit_log(
            user=request.user,
            action="soft_delete",
            model_name="Product",
            object_id=product.id,
            description=(f"Deactivated Product " f"{product.name}"),
            request=request,
        )

        return Response(
            {"success": True, "message": "Product deactivated successfully"},
            status=status.HTTP_200_OK,
        )


# =========================================================
# PRODUCT ACTIVATE
# =========================================================


class ProductActivateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, request, pk):

        queryset = get_product_queryset(request.user, request)

        return queryset.filter(id=pk).first()

    def patch(self, request, pk):

        product = self.get_object(request, pk)

        if not product:

            return Response(
                {"success": False, "message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        check_subscription_write_access(request.user.retailer)

        if product.is_active:

            return Response(
                {"success": False, "message": "Product already active"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product.is_active = True

        product.save(update_fields=["is_active"])

        create_audit_log(
            user=request.user,
            action="restore",
            model_name="Product",
            object_id=product.id,
            description=(f"Activated Product " f"{product.name}"),
            request=request,
        )

        return Response(
            {"success": True, "message": "Product activated successfully"},
            status=status.HTTP_200_OK,
        )


# =========================================================
# PRODUCT HARD DELETE
# =========================================================


class ProductDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get_object(self, request, pk):

        queryset = get_product_queryset(request.user, request)

        return queryset.filter(id=pk).first()

    def delete(self, request, pk):

        product = self.get_object(request, pk)

        if not product:

            return Response(
                {"success": False, "message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        check_subscription_write_access(request.user.retailer)

        product_name = product.name
        product_id = product.id

        product.delete()

        create_audit_log(
            user=request.user,
            action="delete",
            model_name="Product",
            object_id=product_id,
            description=(f"Permanently Deleted Product " f"{product_name}"),
            request=request,
        )

        return Response(
            {"success": True, "message": "Product deleted permanently"},
            status=status.HTTP_200_OK,
        )
