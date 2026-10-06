from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied

from masters.models import Supplier
from masters.serializers import SupplierSerializer

from branches.models import Branch

from accounts.permissions import IsAdmin, IsRetailerOwnerOrPlatformOwner

from subscriptions.utils import check_subscription_write_access
from accounts.views import create_audit_log

# =========================================================
# BASE QUERYSET HELPER
# =========================================================


def get_supplier_queryset(user, request):

    queryset = Supplier.objects.prefetch_related("branches").select_related(
        "retailer", "branch"
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
# CREATE
# =========================================================


class SupplierCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):

        user = request.user

        # =================================================
        # SUBSCRIPTION CHECK
        # =================================================

        if not user.is_superuser:

            check_subscription_write_access(user.retailer)

        serializer = SupplierSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        # =================================================
        # PLATFORM OWNER
        # =================================================

        if user.is_superuser:

            retailer_id = request.data.get("retailer")

            branch_ids = request.data.get("branches", [])

            if not retailer_id:

                raise ValidationError({"retailer": "Retailer is required"})

            if not branch_ids:

                raise ValidationError({"branches": ("At least one branch is required")})

            branches = Branch.objects.filter(retailer_id=retailer_id, id__in=branch_ids)

            if branches.count() != len(branch_ids):

                raise ValidationError({"branches": "Invalid branch ids"})

            supplier = serializer.save(retailer_id=retailer_id)

            supplier.branches.set(branches)

        # =================================================
        # RETAILER USER
        # =================================================

        else:

            supplier = serializer.save(retailer=user.retailer, branch=user.branch)

            supplier.branches.set([user.branch])

        # =================================================
        # AUDIT LOG
        # =================================================

        create_audit_log(
            user=user,
            action="create",
            model_name="Supplier",
            object_id=supplier.id,
            description=(f"Created Supplier " f"{supplier.name}"),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Supplier created successfully",
                "data": SupplierSerializer(supplier).data,
            },
            status=status.HTTP_201_CREATED,
        )


# =========================================================
# LIST
# =========================================================


class SupplierListAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        user = request.user

        queryset = get_supplier_queryset(user, request)

        # =================================================
        # ADMIN / STAFF BRANCH RESTRICTION
        # =================================================

        if not user.is_superuser:

            queryset = queryset.filter(branches=user.branch)

        # =================================================
        # FILTER PARAMETERS
        # =================================================

        is_active = request.query_params.get("is_active")

        search = request.query_params.get("search")

        city = request.query_params.get("city")

        state = request.query_params.get("state")

        branch = request.query_params.get("branch")

        # =================================================
        # ACTIVE FILTER
        # =================================================

        if is_active is not None:

            queryset = queryset.filter(is_active=is_active.lower() == "true")

        # =================================================
        # CITY FILTER
        # =================================================

        if city:

            queryset = queryset.filter(city__icontains=city)

        # =================================================
        # STATE FILTER
        # =================================================

        if state:

            queryset = queryset.filter(state__icontains=state)

        # =================================================
        # BRANCH FILTER
        # =================================================

        if branch:

            queryset = queryset.filter(branches__id=branch)

        # =================================================
        # SEARCH
        # =================================================

        if search:

            queryset = queryset.filter(name__icontains=search)

        # =================================================
        # DISTINCT + ORDER
        # =================================================

        queryset = queryset.distinct().order_by("-id")

        serializer = SupplierSerializer(queryset, many=True)

        return Response(
            {"success": True, "count": queryset.count(), "data": serializer.data},
            status=status.HTTP_200_OK,
        )


# =========================================================
# DETAIL
# =========================================================


class SupplierDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, request, pk):

        queryset = get_supplier_queryset(request.user, request)

        supplier = queryset.filter(id=pk).first()

        if not supplier:

            raise ValidationError({"detail": "Supplier not found"})

        user = request.user

        # =================================================
        # PLATFORM OWNER
        # =================================================

        if user.is_superuser:

            return supplier

        # =================================================
        # BRANCH ACCESS
        # =================================================

        if user.branch in supplier.branches.all():

            return supplier

        raise PermissionDenied("You do not have access to this supplier.")

    def get(self, request, pk):

        supplier = self.get_object(request, pk)

        serializer = SupplierSerializer(supplier)

        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


# =========================================================
# UPDATE
# =========================================================


class SupplierUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, request, pk):

        queryset = get_supplier_queryset(request.user, request)

        supplier = queryset.filter(id=pk).first()

        if not supplier:

            raise ValidationError({"detail": "Supplier not found"})

        user = request.user

        # =================================================
        # PLATFORM OWNER
        # =================================================

        if user.is_superuser:

            return supplier

        # =================================================
        # BRANCH ACCESS
        # =================================================

        if user.branch in supplier.branches.all():

            return supplier

        raise PermissionDenied("Cannot update this supplier")

    def put(self, request, pk):

        return self.update_supplier(request, pk, partial=False)

    def patch(self, request, pk):

        return self.update_supplier(request, pk, partial=True)

    def update_supplier(self, request, pk, partial=False):

        user = request.user

        supplier = self.get_object(request, pk)

        # =================================================
        # SUBSCRIPTION CHECK
        # =================================================

        if not user.is_superuser:

            check_subscription_write_access(user.retailer)

        old_name = supplier.name

        serializer = SupplierSerializer(supplier, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)

        updated_supplier = serializer.save()

        # =================================================
        # RETAILER USER BRANCH
        # =================================================

        if not user.is_superuser:

            updated_supplier.branches.set([user.branch])

        # =================================================
        # AUDIT LOG
        # =================================================

        create_audit_log(
            user=user,
            action="update",
            model_name="Supplier",
            object_id=updated_supplier.id,
            description=(
                f"Updated Supplier from " f"{old_name} to " f"{updated_supplier.name}"
            ),
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Supplier updated successfully",
                "data": SupplierSerializer(updated_supplier).data,
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# SOFT DELETE
# =========================================================


class SupplierSoftDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, request, pk):

        queryset = get_supplier_queryset(request.user, request)

        supplier = queryset.filter(id=pk).first()

        if not supplier:

            raise ValidationError({"detail": "Supplier not found"})

        user = request.user

        # =================================================
        # PLATFORM OWNER
        # =================================================

        if user.is_superuser:

            return supplier

        # =================================================
        # BRANCH ACCESS
        # =================================================

        if user.branch in supplier.branches.all():

            return supplier

        raise PermissionDenied("Permission denied")

    def patch(self, request, pk):

        user = request.user

        supplier = self.get_object(request, pk)

        # =================================================
        # ALREADY INACTIVE
        # =================================================

        if not supplier.is_active:

            return Response(
                {"success": False, "message": "Supplier already inactive"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # =================================================
        # SUBSCRIPTION CHECK
        # =================================================

        if not user.is_superuser:

            check_subscription_write_access(user.retailer)

        # =================================================
        # DEACTIVATE
        # =================================================

        supplier.is_active = False

        supplier.save(update_fields=["is_active"])

        # =================================================
        # AUDIT LOG
        # =================================================

        create_audit_log(
            user=user,
            action="soft_delete",
            model_name="Supplier",
            object_id=supplier.id,
            description=(f"Deactivated Supplier " f"{supplier.name}"),
            request=request,
        )

        return Response(
            {"success": True, "message": "Supplier deactivated successfully"},
            status=status.HTTP_200_OK,
        )


# =========================================================
# ACTIVATE
# =========================================================


class SupplierActivateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, request, pk):

        queryset = get_supplier_queryset(request.user, request)

        supplier = queryset.filter(id=pk).first()

        if not supplier:

            raise ValidationError({"detail": "Supplier not found"})

        user = request.user

        # =================================================
        # PLATFORM OWNER
        # =================================================

        if user.is_superuser:

            return supplier

        # =================================================
        # BRANCH ACCESS
        # =================================================

        if user.branch in supplier.branches.all():

            return supplier

        raise PermissionDenied("Permission denied")

    def patch(self, request, pk):

        user = request.user

        supplier = self.get_object(request, pk)

        # =================================================
        # ALREADY ACTIVE
        # =================================================

        if supplier.is_active:

            return Response(
                {"success": False, "message": "Supplier already active"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # =================================================
        # SUBSCRIPTION CHECK
        # =================================================

        if not user.is_superuser:

            check_subscription_write_access(user.retailer)

        # =================================================
        # ACTIVATE
        # =================================================

        supplier.is_active = True

        supplier.save(update_fields=["is_active"])

        # =================================================
        # AUDIT LOG
        # =================================================

        create_audit_log(
            user=user,
            action="activate",
            model_name="Supplier",
            object_id=supplier.id,
            description=(f"Activated Supplier " f"{supplier.name}"),
            request=request,
        )

        return Response(
            {"success": True, "message": "Supplier activated successfully"},
            status=status.HTTP_200_OK,
        )


# =========================================================
# HARD DELETE
# =========================================================


class SupplierDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    def get_object(self, request, pk):

        queryset = get_supplier_queryset(request.user, request)

        supplier = queryset.filter(id=pk).first()

        if not supplier:

            raise ValidationError({"detail": "Supplier not found"})

        user = request.user

        # =================================================
        # PLATFORM OWNER
        # =================================================

        if user.is_superuser:

            return supplier

        # =================================================
        # BRANCH ACCESS
        # =================================================

        if user.branch in supplier.branches.all():

            return supplier

        raise PermissionDenied("You do not have access to this supplier.")

    def delete(self, request, pk):

        user = request.user

        supplier = self.get_object(request, pk)

        # =================================================
        # SUBSCRIPTION CHECK
        # =================================================

        if not user.is_superuser:

            check_subscription_write_access(user.retailer)

        supplier_id = supplier.id
        supplier_name = supplier.name

        # =================================================
        # DELETE
        # =================================================

        supplier.delete()

        # =================================================
        # AUDIT LOG
        # =================================================

        create_audit_log(
            user=user,
            action="delete",
            model_name="Supplier",
            object_id=supplier_id,
            description=(f"Permanently Deleted Supplier " f"{supplier_name}"),
            request=request,
        )

        return Response(
            {"success": True, "message": "Supplier deleted permanently"},
            status=status.HTTP_200_OK,
        )
