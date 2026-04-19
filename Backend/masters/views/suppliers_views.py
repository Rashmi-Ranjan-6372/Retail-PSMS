from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from masters.models import Supplier
from masters.serializers import SupplierSerializer
from branches.models import Branch
from accounts.permissions import IsAdmin
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied

# ================= CREATE ================= #

class SupplierCreateView(generics.CreateAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_superuser:
            branch_ids = self.request.data.get("branches", [])

            if not branch_ids:
                raise ValidationError({
                    "branches": "This field is required for super admin"
                })

            branches = Branch.objects.filter(id__in=branch_ids)

            if not branches.exists():
                raise ValidationError({
                    "branches": "Invalid branch IDs"
                })

            supplier = serializer.save()
            supplier.branches.set(branches)

        else:
            supplier = serializer.save()
            supplier.branches.set([user.branch])


# ================= LIST ================= #
class SupplierListView(generics.ListAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Supplier.objects.all()

        else:
            queryset = Supplier.objects.filter(
                branches=user.branch
            )

        is_active = self.request.query_params.get("is_active")
        search = self.request.query_params.get("search")

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset.order_by("-id")

# ================= DETAIL ================= #
class SupplierDetailView(generics.RetrieveAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Supplier.objects.all()

    def get_object(self):
        supplier = super().get_object()
        user = self.request.user

        if user.is_superuser or user.branch in supplier.branches.all():
            return supplier

        raise PermissionDenied("You do not have access to this supplier.")


# ================= UPDATE ================= #
class SupplierUpdateView(generics.UpdateAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Supplier.objects.all()

    def perform_update(self, serializer):
        user = self.request.user
        supplier = self.get_object()

        if not user.is_superuser and user.branch not in supplier.branches.all():
            raise PermissionDenied("Cannot update this supplier")

        updated_supplier = serializer.save()

        # Admin → restrict branch
        if not user.is_superuser:
            updated_supplier.branches.set([user.branch])


# ================= SOFT DELETE ================= #
class SupplierSoftDeleteView(generics.UpdateAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Supplier.objects.all()

    def patch(self, request, *args, **kwargs):
        supplier = self.get_object()
        user = request.user

        if not user.is_superuser and user.branch not in supplier.branches.all():
            return Response({"error": "Permission denied"}, status=403)

        supplier.is_active = False
        supplier.save()

        return Response({
            "success": True,
            "message": "Supplier deactivated"
        })

# ================= HARD DELETE ================= #
class SupplierDeleteView(generics.DestroyAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Supplier.objects.all()

    def destroy(self, request, *args, **kwargs):
        supplier = self.get_object()
        user = request.user

        if not user.is_superuser:
            return Response(
                {"error": "Only super admin can delete"},
                status=403
            )

        supplier.delete()

        return Response({
            "success": True,
            "message": "Supplier deleted permanently"
        })