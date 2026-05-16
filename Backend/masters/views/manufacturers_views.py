from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from masters.models import Manufacturer
from masters.serializers import ManufacturerSerializer

from accounts.permissions import (
    IsAdmin,
    IsSuperAdmin
)


# =========================================================
# HELPER QUERYSET
# =========================================================

def get_manufacturer_queryset(user):

    # PLATFORM OWNER
    if user.is_superuser:
        return Manufacturer.objects.all()

    # SUPERADMIN -> RETAILER LEVEL
    if user.role == "superadmin":
        return Manufacturer.objects.filter(
            retailer=user.retailer
        )

    # ADMIN / STAFF -> BRANCH LEVEL
    return Manufacturer.objects.filter(
        retailer=user.retailer,
        branch=user.branch
    )


# =========================================================
# CREATE
# =========================================================

class ManufacturerCreateView(generics.CreateAPIView):

    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):

        serializer.save(
            retailer=self.request.user.retailer,
            branch=self.request.user.branch
        )

    def create(self, request, *args, **kwargs):

        response = super().create(request, *args, **kwargs)

        return Response({
            "success": True,
            "message": "Manufacturer created successfully",
            "data": response.data
        }, status=status.HTTP_201_CREATED)


# =========================================================
# LIST
# =========================================================

class ManufacturerListView(generics.ListAPIView):

    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):

        queryset = get_manufacturer_queryset(
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

class ManufacturerDetailView(generics.RetrieveAPIView):

    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):

        return get_manufacturer_queryset(
            self.request.user
        )

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(instance)

        return Response({
            "success": True,
            "data": serializer.data
        })


# =========================================================
# UPDATE
# =========================================================

class ManufacturerUpdateView(generics.UpdateAPIView):

    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):

        return get_manufacturer_queryset(
            self.request.user
        )

    def update(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response({
            "success": True,
            "message": "Manufacturer updated successfully",
            "data": serializer.data
        })


# =========================================================
# SOFT DELETE
# =========================================================

class ManufacturerSoftDeleteView(generics.UpdateAPIView):

    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):

        return get_manufacturer_queryset(
            self.request.user
        )

    def patch(self, request, *args, **kwargs):

        manufacturer = self.get_object()

        if not manufacturer.is_active:

            return Response({
                "success": False,
                "message": "Manufacturer already inactive"
            }, status=status.HTTP_400_BAD_REQUEST)

        manufacturer.is_active = False
        manufacturer.save()

        return Response({
            "success": True,
            "message": "Manufacturer deactivated successfully"
        })


# =========================================================
# RESTORE
# =========================================================

class ManufacturerRestoreView(generics.UpdateAPIView):

    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):

        return get_manufacturer_queryset(
            self.request.user
        )

    def patch(self, request, *args, **kwargs):

        manufacturer = self.get_object()

        if manufacturer.is_active:

            return Response({
                "success": False,
                "message": "Manufacturer already active"
            }, status=status.HTTP_400_BAD_REQUEST)

        manufacturer.is_active = True
        manufacturer.save()

        return Response({
            "success": True,
            "message": "Manufacturer restored successfully"
        })


# =========================================================
# HARD DELETE
# =========================================================

class ManufacturerDeleteView(generics.DestroyAPIView):

    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get_queryset(self):

        return get_manufacturer_queryset(
            self.request.user
        )

    def destroy(self, request, *args, **kwargs):

        manufacturer = self.get_object()

        manufacturer.delete()

        return Response({
            "success": True,
            "message": "Manufacturer deleted permanently"
        }, status=status.HTTP_200_OK)