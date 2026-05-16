from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from masters.models import Category
from masters.serializers import ProductCategorySerializer

from accounts.permissions import IsAdmin


# =========================================================
# HELPER QUERYSET
# =========================================================

def get_category_queryset(user):

    # PLATFORM OWNER
    if user.is_superuser:
        return Category.objects.all()

    # SUPERADMIN -> RETAILER LEVEL
    if user.role == "superadmin":
        return Category.objects.filter(
            retailer=user.retailer
        )

    # ADMIN / STAFF -> BRANCH LEVEL
    return Category.objects.filter(
        retailer=user.retailer,
        branch=user.branch
    )


# =========================================================
# PRODUCT CATEGORY LIST + CREATE
# =========================================================

class ProductCategoryListCreateView(
    generics.ListCreateAPIView
):

    serializer_class = ProductCategorySerializer
    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):

        queryset = get_category_queryset(
            self.request.user
        )

        is_active = self.request.query_params.get(
            "is_active"
        )

        search = self.request.query_params.get(
            "search"
        )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        return queryset.order_by("name")

    def perform_create(self, serializer):

        serializer.save(
            retailer=self.request.user.retailer,
            branch=self.request.user.branch
        )

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

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        self.perform_create(serializer)

        return Response({
            "success": True,
            "message": "Category created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


# =========================================================
# PRODUCT CATEGORY DETAIL / UPDATE / DELETE
# =========================================================

class ProductCategoryRetrieveUpdateDeleteView(
    generics.RetrieveUpdateDestroyAPIView
):

    serializer_class = ProductCategorySerializer
    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):

        return get_category_queryset(
            self.request.user
        )

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance
        )

        return Response({
            "success": True,
            "data": serializer.data
        })

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop(
            "partial",
            False
        )

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response({
            "success": True,
            "message": "Category updated successfully",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.delete()

        return Response({
            "success": True,
            "message": "Category deleted successfully"
        }, status=status.HTTP_200_OK)