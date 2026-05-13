from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from masters.models import Product
from masters.serializers import ProductSerializer

from accounts.permissions import IsAdmin, IsSuperAdmin


# ================= CREATE ================= #

class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,IsAdmin]

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,IsAdmin]

    def get_queryset(self):
        queryset = Product.objects.select_related("category","manufacturer").all()
        is_active = self.request.query_params.get("is_active")
        category = self.request.query_params.get("category")
        manufacturer = self.request.query_params.get("manufacturer")
        search = self.request.query_params.get("search")
        prescription_required = self.request.query_params.get("prescription_required")

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

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        return queryset.order_by("name")


# ================= DETAIL ================= #

class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,IsAdmin]
    queryset = Product.objects.select_related("category","manufacturer").all()


# ================= UPDATE ================= #

class ProductUpdateView(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,IsAdmin]
    queryset = Product.objects.all()

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


# ================= SOFT DELETE ================= #

class ProductSoftDeleteView(generics.UpdateAPIView):

    serializer_class = ProductSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    queryset = Product.objects.all()

    def patch(self, request, *args, **kwargs):

        product = self.get_object()

        if not product.is_active:
            return Response({
                "success": False,
                "message": "Product already inactive"
            }, status=400)

        product.is_active = False

        product.save()

        return Response({
            "success": True,
            "message": "Product deactivated successfully"
        })


# ================= HARD DELETE ================= #

class ProductDeleteView(generics.DestroyAPIView):

    serializer_class = ProductSerializer

    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin
    ]

    queryset = Product.objects.all()

    def destroy(self, request, *args, **kwargs):

        product = self.get_object()

        product.delete()

        return Response({
            "success": True,
            "message": "Product deleted permanently"
        }, status=status.HTTP_200_OK)