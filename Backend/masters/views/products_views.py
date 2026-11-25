from django.utils import timezone
from django.db.models import Q
from django.db.models.deletion import ProtectedError

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from accounts.permissions import IsAdmin
from masters.models import Product
from masters.serializers import ProductSerializer

from subscriptions.utils import check_subscription_write_access
from accounts.views import create_audit_log
from rest_framework.permissions import IsAuthenticated

# =========================================================
# SUBSCRIPTION CHECK
# =========================================================


def check_product_subscription(user):

    if user.is_superuser:
        return

    if not getattr(user, "retailer_id", None):
        raise ValueError("Retailer account is not assigned.")

    check_subscription_write_access(user.retailer)


# =========================================================
# BASE QUERYSET HELPER
# =========================================================


def get_product_queryset(user, request):

    queryset = Product.objects.select_related("category", "manufacturer", "retailer")

    if user.is_superuser:

        retailer_id = request.query_params.get("retailer")

        if retailer_id:
            queryset = queryset.filter(retailer_id=retailer_id)

        return queryset

    if not getattr(user, "retailer_id", None):
        return Product.objects.none()

    return queryset.filter(retailer=user.retailer)


# =========================================================
# PRODUCT CREATE
# =========================================================


class ProductCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):

        user = request.user

        try:
            check_product_subscription(user)

            if user.is_superuser:
                retailer_id = request.data.get("retailer")

                if not retailer_id:
                    return Response(
                        {"success": False, "message": "Retailer ID is required."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                from accounts.models import Retailer

                try:
                    retailer = Retailer.objects.get(id=retailer_id)
                except Retailer.DoesNotExist:
                    return Response(
                        {"success": False, "message": "Retailer not found."},
                        status=status.HTTP_404_NOT_FOUND,
                    )

            else:
                retailer = user.retailer

            serializer = ProductSerializer(
                data=request.data, context={"request": request}
            )

            serializer.is_valid(raise_exception=True)

            product = serializer.save(retailer=retailer)

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
                    "message": "Product created successfully.",
                    "data": ProductSerializer(product).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


# =========================================================
# PRODUCT LIST
# =========================================================


class ProductListAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        queryset = get_product_queryset(request.user, request)

        is_active = request.query_params.get("is_active")
        category = request.query_params.get("category")
        manufacturer = request.query_params.get("manufacturer")
        search = request.query_params.get("search")
        prescription_required = request.query_params.get("prescription_required")

        if is_active is not None:

            if is_active.lower() not in ["true", "false"]:
                return Response(
                    {"success": False, "message": "is_active must be true or false."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            queryset = queryset.filter(is_active=(is_active.lower() == "true"))

        else:
            queryset = queryset.filter(is_active=True)

        if category:
            queryset = queryset.filter(category_id=category)

        if manufacturer:
            queryset = queryset.filter(manufacturer_id=manufacturer)

        if prescription_required is not None:

            if prescription_required.lower() not in ["true", "false"]:
                return Response(
                    {
                        "success": False,
                        "message": "prescription_required must be true or false.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            queryset = queryset.filter(
                prescription_required=(prescription_required.lower() == "true")
            )

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(strength__icontains=search)
                | Q(category__name__icontains=search)
                | Q(manufacturer__name__icontains=search)
            )

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
                {"success": False, "message": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProductSerializer(product)

        return Response(
            {
                "success": True,
                "message": "Product fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
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
                {"success": False, "message": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            check_product_subscription(request.user)

            if not product.is_active:
                return Response(
                    {
                        "success": False,
                        "message": "Inactive product cannot be updated. Restore it first.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            old_name = product.name

            serializer = ProductSerializer(
                product,
                data=request.data,
                partial=partial,
                context={"request": request},
            )

            serializer.is_valid(raise_exception=True)

            product = serializer.save()

            create_audit_log(
                user=request.user,
                action="update",
                model_name="Product",
                object_id=product.id,
                description=f"Updated Product from {old_name} to {product.name}",
                request=request,
            )

            return Response(
                {
                    "success": True,
                    "message": "Product updated successfully.",
                    "data": ProductSerializer(product).data,
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


# =========================================================
# PRODUCT SOFT DELETE / DEACTIVATE
# =========================================================


class ProductSoftDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):

        product = get_product_queryset(request.user, request).filter(id=pk).first()

        if not product:
            return Response(
                {"success": False, "message": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            check_product_subscription(request.user)

            if not product.is_active:
                return Response(
                    {"success": False, "message": "Product is already inactive."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            product.is_active = False
            product.deleted_at = timezone.now()

            product.save(update_fields=["is_active", "deleted_at", "updated_at"])

            create_audit_log(
                user=request.user,
                action="soft_delete",
                model_name="Product",
                object_id=product.id,
                description=f"Deactivated Product {product.name}",
                request=request,
            )

            return Response(
                {"success": True, "message": "Product deactivated successfully."},
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


# =========================================================
# PRODUCT RESTORE / ACTIVATE
# =========================================================


class ProductActivateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):

        product = get_product_queryset(request.user, request).filter(id=pk).first()

        if not product:
            return Response(
                {"success": False, "message": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            check_product_subscription(request.user)

            if product.is_active:
                return Response(
                    {"success": False, "message": "Product is already active."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            product.is_active = True
            product.deleted_at = None

            product.save(update_fields=["is_active", "deleted_at", "updated_at"])

            create_audit_log(
                user=request.user,
                action="restore",
                model_name="Product",
                object_id=product.id,
                description=f"Restored Product {product.name}",
                request=request,
            )

            return Response(
                {"success": True, "message": "Product restored successfully."},
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


# =========================================================
# PRODUCT HARD DELETE
# =========================================================


class ProductDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]
    
    def delete(self, request, pk):

        product = get_product_queryset(request.user, request).filter(id=pk).first()

        if not product:
            return Response(
                {"success": False, "message": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            check_product_subscription(request.user)

            product_name = product.name
            product_id = product.id

            product.delete()

            create_audit_log(
                user=request.user,
                action="delete",
                model_name="Product",
                object_id=product_id,
                description=f"Permanently deleted Product {product_name}",
                request=request,
            )

            return Response(
                {"success": True, "message": "Product deleted permanently."},
                status=status.HTTP_200_OK,
            )

        except ProtectedError:
            return Response(
                {
                    "success": False,
                    "message": "This product is already used in inventory or other records. Deactivate it instead.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ValueError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
