from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import (
    ValidationError,
    PermissionDenied
)

from masters.models import Supplier
from masters.serializers import SupplierSerializer
from branches.models import Branch

from accounts.permissions import (
    IsAdmin,
    IsRetailerOwnerOrPlatformOwner
)


# =========================================================
# BASE RETAILER MIXIN
# =========================================================

class RetailerSupplierMixin:

    def get_queryset(self):

        user = self.request.user

        queryset = Supplier.objects.prefetch_related(
            "branches"
        ).select_related(
            "retailer",
            "branch"
        )

        # ================= PLATFORM OWNER =================
        if user.is_superuser:

            retailer_id = self.request.query_params.get(
                "retailer"
            )

            if retailer_id:
                queryset = queryset.filter(
                    retailer_id=retailer_id
                )

            return queryset

        # ================= RETAILER USERS =================
        return queryset.filter(
            retailer=user.retailer
        )


# =========================================================
# CREATE
# =========================================================

class SupplierCreateView(
    RetailerSupplierMixin,
    generics.CreateAPIView
):

    serializer_class = SupplierSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def perform_create(self, serializer):

        user = self.request.user

        # ================= SUPERUSER =================
        if user.is_superuser:

            retailer_id = self.request.data.get(
                "retailer"
            )

            branch_ids = self.request.data.get(
                "branches",
                []
            )

            if not retailer_id:
                raise ValidationError({
                    "retailer":
                    "Retailer is required"
                })

            if not branch_ids:
                raise ValidationError({
                    "branches":
                    "At least one branch is required"
                })

            branches = Branch.objects.filter(
                retailer_id=retailer_id,
                id__in=branch_ids
            )

            if branches.count() != len(branch_ids):
                raise ValidationError({
                    "branches":
                    "Invalid branch ids"
                })

            supplier = serializer.save(
                retailer_id=retailer_id
            )

            supplier.branches.set(branches)

        # ================= RETAILER USERS =================
        else:

            supplier = serializer.save(
                retailer=user.retailer,
                branch=user.branch
            )

            supplier.branches.set([user.branch])

    def create(self, request, *args, **kwargs):

        response = super().create(
            request,
            *args,
            **kwargs
        )

        return Response({
            "success": True,
            "message": "Supplier created successfully",
            "data": response.data
        }, status=status.HTTP_201_CREATED)


# =========================================================
# LIST
# =========================================================

class SupplierListView(
    RetailerSupplierMixin,
    generics.ListAPIView
):

    serializer_class = SupplierSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        user = self.request.user

        # ================= ADMIN / STAFF =================
        if not user.is_superuser:

            queryset = queryset.filter(
                branches=user.branch
            )

        is_active = self.request.query_params.get(
            "is_active"
        )

        search = self.request.query_params.get(
            "search"
        )

        city = self.request.query_params.get(
            "city"
        )

        state = self.request.query_params.get(
            "state"
        )

        branch = self.request.query_params.get(
            "branch"
        )

        # ================= FILTERS =================

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        if city:
            queryset = queryset.filter(
                city__icontains=city
            )

        if state:
            queryset = queryset.filter(
                state__icontains=state
            )

        if branch:
            queryset = queryset.filter(
                branches__id=branch
            )

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        return queryset.distinct().order_by("-id")

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

class SupplierDetailView(
    RetailerSupplierMixin,
    generics.RetrieveAPIView
):

    serializer_class = SupplierSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):
        return super().get_queryset()

    def get_object(self):

        supplier = super().get_object()

        user = self.request.user

        if user.is_superuser:
            return supplier

        if user.branch in supplier.branches.all():
            return supplier

        raise PermissionDenied(
            "You do not have access to this supplier."
        )


# =========================================================
# UPDATE
# =========================================================

class SupplierUpdateView(
    RetailerSupplierMixin,
    generics.UpdateAPIView
):

    serializer_class = SupplierSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):
        return super().get_queryset()

    def perform_update(self, serializer):

        user = self.request.user

        supplier = self.get_object()

        if (
            not user.is_superuser and
            user.branch not in supplier.branches.all()
        ):
            raise PermissionDenied(
                "Cannot update this supplier"
            )

        updated_supplier = serializer.save()

        # ================= ADMIN RESTRICTION =================
        if not user.is_superuser:
            updated_supplier.branches.set(
                [user.branch]
            )

    def update(self, request, *args, **kwargs):

        response = super().update(
            request,
            *args,
            **kwargs
        )

        return Response({
            "success": True,
            "message": "Supplier updated successfully",
            "data": response.data
        })


# =========================================================
# SOFT DELETE
# =========================================================

class SupplierSoftDeleteView(
    RetailerSupplierMixin,
    generics.UpdateAPIView
):

    serializer_class = SupplierSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):
        return super().get_queryset()

    def patch(self, request, *args, **kwargs):

        supplier = self.get_object()

        user = request.user

        if (
            not user.is_superuser and
            user.branch not in supplier.branches.all()
        ):
            raise PermissionDenied(
                "Permission denied"
            )

        if not supplier.is_active:
            return Response({
                "success": False,
                "message": "Supplier already inactive"
            }, status=status.HTTP_400_BAD_REQUEST)

        supplier.is_active = False

        supplier.save(update_fields=["is_active"])

        return Response({
            "success": True,
            "message": "Supplier deactivated successfully"
        })


# =========================================================
# ACTIVATE
# =========================================================

class SupplierActivateView(
    RetailerSupplierMixin,
    generics.UpdateAPIView
):

    serializer_class = SupplierSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):
        return super().get_queryset()

    def patch(self, request, *args, **kwargs):

        supplier = self.get_object()

        if supplier.is_active:
            return Response({
                "success": False,
                "message": "Supplier already active"
            }, status=status.HTTP_400_BAD_REQUEST)

        supplier.is_active = True

        supplier.save(update_fields=["is_active"])

        return Response({
            "success": True,
            "message": "Supplier activated successfully"
        })


# =========================================================
# HARD DELETE
# =========================================================

class SupplierDeleteView(
    RetailerSupplierMixin,
    generics.DestroyAPIView
):

    serializer_class = SupplierSerializer

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner
    ]

    def get_queryset(self):
        return super().get_queryset()

    def destroy(self, request, *args, **kwargs):

        supplier = self.get_object()

        supplier.delete()

        return Response({
            "success": True,
            "message": "Supplier deleted permanently"
        }, status=status.HTTP_200_OK)