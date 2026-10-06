from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from masters.models import Category
from masters.serializers import ProductCategorySerializer

from accounts.permissions import IsAdmin
from subscriptions.utils import check_subscription_write_access
from accounts.views import create_audit_log

# =========================================================
# HELPER QUERYSET
# =========================================================


def get_category_queryset(user):

    # PLATFORM OWNER
    if user.is_superuser:
        return Category.objects.all()

    # SUPERADMIN -> RETAILER LEVEL
    if user.role == "superadmin":
        return Category.objects.filter(retailer=user.retailer)

    # ADMIN / STAFF -> BRANCH LEVEL
    return Category.objects.filter(retailer=user.retailer, branch=user.branch)


# =========================================================
# PRODUCT CATEGORY LIST + CREATE
# =========================================================


class ProductCategoryListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    # =====================================================
    # GET - LIST ALL CATEGORIES
    # =====================================================

    def get(self, request):

        queryset = get_category_queryset(request.user)

        # Filter by active status
        is_active = request.query_params.get("is_active")

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        # Search by category name
        search = request.query_params.get("search")

        if search:
            queryset = queryset.filter(name__icontains=search)

        queryset = queryset.order_by("name")

        serializer = ProductCategorySerializer(queryset, many=True)

        return Response(
            {"success": True, "count": queryset.count(), "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    # =====================================================
    # POST - CREATE CATEGORY
    # =====================================================

    def post(self, request):

        check_subscription_write_access(request.user.retailer)

        serializer = ProductCategorySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        category = serializer.save(
            retailer=request.user.retailer, branch=request.user.branch
        )

        create_audit_log(
            user=request.user,
            action="create",
            model_name="Category",
            object_id=category.id,
            description=f"Created Category {category.name}",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Category created successfully",
                "data": ProductCategorySerializer(category).data,
            },
            status=status.HTTP_201_CREATED,
        )


# =========================================================
# PRODUCT CATEGORY DETAIL / UPDATE / DELETE
# =========================================================


class ProductCategoryDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    # =====================================================
    # HELPER - GET CATEGORY
    # =====================================================

    def get_object(self, request, pk):

        queryset = get_category_queryset(request.user)

        return queryset.filter(id=pk).first()

    # =====================================================
    # GET - RETRIEVE CATEGORY
    # =====================================================

    def get(self, request, pk):

        category = self.get_object(request, pk)

        if not category:
            return Response(
                {"success": False, "message": "Category not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProductCategorySerializer(category)

        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    # =====================================================
    # PUT - FULL UPDATE
    # =====================================================

    def put(self, request, pk):

        category = self.get_object(request, pk)

        if not category:
            return Response(
                {"success": False, "message": "Category not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        check_subscription_write_access(request.user.retailer)

        old_name = category.name

        serializer = ProductCategorySerializer(
            category, data=request.data, partial=False
        )

        serializer.is_valid(raise_exception=True)

        category = serializer.save()

        create_audit_log(
            user=request.user,
            action="update",
            model_name="Category",
            object_id=category.id,
            description=(f"Updated Category from " f"{old_name} to {category.name}"),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Category updated successfully",
                "data": ProductCategorySerializer(category).data,
            },
            status=status.HTTP_200_OK,
        )

    # =====================================================
    # PATCH - PARTIAL UPDATE
    # =====================================================

    def patch(self, request, pk):

        category = self.get_object(request, pk)

        if not category:
            return Response(
                {"success": False, "message": "Category not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        check_subscription_write_access(request.user.retailer)

        old_name = category.name

        serializer = ProductCategorySerializer(
            category, data=request.data, partial=True
        )

        serializer.is_valid(raise_exception=True)

        category = serializer.save()

        create_audit_log(
            user=request.user,
            action="update",
            model_name="Category",
            object_id=category.id,
            description=(f"Updated Category from " f"{old_name} to {category.name}"),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Category updated successfully",
                "data": ProductCategorySerializer(category).data,
            },
            status=status.HTTP_200_OK,
        )

    # =====================================================
    # DELETE - DELETE CATEGORY
    # =====================================================

    def delete(self, request, pk):

        category = self.get_object(request, pk)

        if not category:
            return Response(
                {"success": False, "message": "Category not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        check_subscription_write_access(request.user.retailer)

        category_name = category.name
        category_id = category.id

        category.delete()

        create_audit_log(
            user=request.user,
            action="delete",
            model_name="Category",
            object_id=category_id,
            description=f"Deleted Category {category_name}",
            request=request,
        )

        return Response(
            {"success": True, "message": "Category deleted successfully"},
            status=status.HTTP_200_OK,
        )
