from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from masters.models import Manufacturer
from masters.serializers import ManufacturerSerializer
from accounts.permissions import IsAdmin, IsSuperAdmin


# ================= CREATE ================= #
class ManufacturerCreateView(generics.CreateAPIView):
    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


# ================= LIST ================= #
class ManufacturerListView(generics.ListAPIView):
    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        queryset = Manufacturer.objects.all()

        # 🔍 Filters
        is_active = self.request.query_params.get("is_active")
        search = self.request.query_params.get("search")

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset.order_by("name")


# ================= DETAIL ================= #
class ManufacturerDetailView(generics.RetrieveAPIView):
    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Manufacturer.objects.all()


# ================= UPDATE ================= #
class ManufacturerUpdateView(generics.UpdateAPIView):
    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Manufacturer.objects.all()

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
            "message": "Manufacturer updated successfully",
            "data": serializer.data
        })


# ================= SOFT DELETE ================= #
class ManufacturerSoftDeleteView(generics.UpdateAPIView):
    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Manufacturer.objects.all()

    def patch(self, request, *args, **kwargs):
        manufacturer = self.get_object()

        if not manufacturer.is_active:
            return Response({
                "success": False,
                "message": "Already inactive"
            }, status=400)

        manufacturer.is_active = False
        manufacturer.save()

        return Response({
            "success": True,
            "message": "Manufacturer deactivated"
        })


# ================= HARD DELETE ================= #
class ManufacturerDeleteView(generics.DestroyAPIView):
    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    queryset = Manufacturer.objects.all()

    def destroy(self, request, *args, **kwargs):
        manufacturer = self.get_object()
        manufacturer.delete()

        return Response({
            "success": True,
            "message": "Manufacturer deleted permanently"
        }, status=status.HTTP_200_OK)