from django.db import transaction
from django.db.models import ProtectedError
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied

from masters.models.suppliers_models import Supplier
from masters.serializers.suppliers_serializers import SupplierSerializer

from branches.models import Branch
from accounts.models import Retailer

from accounts.permissions import IsAdmin, IsRetailerOwnerOrPlatformOwner

from subscriptions.utils import check_subscription_write_access
from accounts.views import create_audit_log

# =========================================================
# RETAILER HELPER
# =========================================================


def get_supplier_retailer(user, request, data=None):

    if user.is_superuser:

        retailer_id = None

        if data:
            retailer_id = data.get("retailer")

        if not retailer_id:
            retailer_id = request.query_params.get("retailer")

        if not retailer_id:
            raise ValidationError({"retailer": "Retailer is required."})

        retailer = Retailer.objects.filter(id=retailer_id).first()

        if not retailer:
            raise ValidationError({"retailer": "Invalid retailer."})

        return retailer

    retailer = getattr(user, "retailer", None)

    if not retailer:
        raise ValidationError("Retailer account is not assigned.")

    return retailer


# =========================================================
# BASE QUERYSET HELPER
# =========================================================


def get_supplier_queryset(user, request):

    queryset = Supplier.objects.select_related("retailer").prefetch_related("branches")

    retailer = get_supplier_retailer(user, request)

    queryset = queryset.filter(retailer=retailer)

    # ================= BRANCH RESTRICTION =================

    if not user.is_superuser:

        user_branch = getattr(user, "branch", None)

        if user_branch:
            queryset = queryset.filter(branches=user_branch)

    return queryset.distinct()


# =========================================================
# BASE OBJECT ACCESS HELPER
# =========================================================


def get_supplier_object(request, pk):

    supplier = get_supplier_queryset(request.user, request).filter(id=pk).first()

    if not supplier:
        raise ValidationError({"detail": "Supplier not found."})

    return supplier


# =========================================================
# SERIALIZER CONTEXT
# =========================================================


def get_supplier_serializer_context(request, retailer):

    return {
        "request": request,
        "retailer": retailer,
    }


# =========================================================
# CREATE
# =========================================================


class SupplierCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):

        user = request.user

        retailer = get_supplier_retailer(user, request, request.data)

        # ================= SUBSCRIPTION CHECK =================

        if not user.is_superuser:
            check_subscription_write_access(retailer)

        # ================= BRANCH VALIDATION =================

        if user.is_superuser or not getattr(user, "branch", None):

            branch_ids = request.data.get("branches", [])

            if not branch_ids:
                raise ValidationError({"branches": "At least one branch is required."})

            if not isinstance(branch_ids, list):
                raise ValidationError(
                    {"branches": "Branches must be a list of branch IDs."}
                )

            branches = Branch.objects.filter(retailer=retailer, id__in=branch_ids)

            if branches.count() != len(set(branch_ids)):
                raise ValidationError(
                    {"branches": "One or more selected branches are invalid."}
                )

        else:
            branches = [user.branch]

        # ================= SERIALIZER =================

        serializer = SupplierSerializer(
            data=request.data,
            context=get_supplier_serializer_context(request, retailer),
        )

        serializer.is_valid(raise_exception=True)

        with transaction.atomic():

            supplier = serializer.save()

        # ================= AUDIT LOG =================

        create_audit_log(
            user=user,
            action="create",
            model_name="Supplier",
            object_id=supplier.id,
            description=f"Created Supplier {supplier.name}",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Supplier created successfully.",
                "data": SupplierSerializer(
                    supplier, context=get_supplier_serializer_context(request, retailer)
                ).data,
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

        retailer = get_supplier_retailer(user, request)

        # ================= FILTER PARAMETERS =================

        is_active = request.query_params.get("is_active")
        search = request.query_params.get("search")
        city = request.query_params.get("city")
        state = request.query_params.get("state")
        branch = request.query_params.get("branch")

        # ================= ACTIVE FILTER =================

        if is_active is not None:

            if is_active.lower() not in ["true", "false"]:
                raise ValidationError({"is_active": "Use true or false."})

            queryset = queryset.filter(is_active=is_active.lower() == "true")

        # ================= CITY FILTER =================

        if city:
            queryset = queryset.filter(city__icontains=city)

        # ================= STATE FILTER =================

        if state:
            queryset = queryset.filter(state__icontains=state)

        # ================= BRANCH FILTER =================

        if branch:

            selected_branch = Branch.objects.filter(
                id=branch, retailer=retailer
            ).first()

            if not selected_branch:
                raise ValidationError({"branch": "Invalid branch."})

            if not user.is_superuser and getattr(user, "branch", None):

                if selected_branch.id != user.branch_id:
                    raise PermissionDenied(
                        "You cannot view suppliers from another branch."
                    )

            queryset = queryset.filter(branches=selected_branch)

        # ================= SEARCH =================

        if search:
            queryset = queryset.filter(name__icontains=search)

        queryset = queryset.distinct().order_by("-id")

        serializer = SupplierSerializer(
            queryset,
            many=True,
            context=get_supplier_serializer_context(request, retailer),
        )

        return Response(
            {
                "success": True,
                "count": queryset.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# DETAIL
# =========================================================


class SupplierDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk):

        supplier = get_supplier_object(request, pk)

        retailer = get_supplier_retailer(request.user, request)

        serializer = SupplierSerializer(
            supplier, context=get_supplier_serializer_context(request, retailer)
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# UPDATE
# =========================================================


class SupplierUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def put(self, request, pk):
        return self.update_supplier(request, pk, partial=False)

    def patch(self, request, pk):
        return self.update_supplier(request, pk, partial=True)

    def update_supplier(self, request, pk, partial=False):

        user = request.user

        supplier = get_supplier_object(request, pk)

        retailer = get_supplier_retailer(user, request)

        # ================= SUBSCRIPTION CHECK =================

        if not user.is_superuser:
            check_subscription_write_access(retailer)

        old_name = supplier.name

        serializer = SupplierSerializer(
            supplier,
            data=request.data,
            partial=partial,
            context=get_supplier_serializer_context(request, retailer),
        )

        serializer.is_valid(raise_exception=True)

        with transaction.atomic():

            updated_supplier = serializer.save()

        # ================= AUDIT LOG =================

        create_audit_log(
            user=user,
            action="update",
            model_name="Supplier",
            object_id=updated_supplier.id,
            description=f"Updated Supplier from {old_name} to {updated_supplier.name}",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Supplier updated successfully.",
                "data": SupplierSerializer(
                    updated_supplier,
                    context=get_supplier_serializer_context(request, retailer),
                ).data,
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# SOFT DELETE
# =========================================================


class SupplierSoftDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):

        user = request.user

        supplier = get_supplier_object(request, pk)

        retailer = get_supplier_retailer(user, request)

        if not supplier.is_active:
            return Response(
                {
                    "success": False,
                    "message": "Supplier already inactive.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_superuser:
            check_subscription_write_access(retailer)

        supplier.is_active = False
        supplier.deleted_at = timezone.now()

        supplier.save(
            update_fields=[
                "is_active",
                "deleted_at",
                "updated_at",
            ]
        )

        create_audit_log(
            user=user,
            action="soft_delete",
            model_name="Supplier",
            object_id=supplier.id,
            description=f"Deactivated Supplier {supplier.name}",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Supplier deactivated successfully.",
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# ACTIVATE
# =========================================================


class SupplierActivateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):

        user = request.user

        supplier = get_supplier_object(request, pk)

        retailer = get_supplier_retailer(user, request)

        if supplier.is_active:
            return Response(
                {
                    "success": False,
                    "message": "Supplier already active.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_superuser:
            check_subscription_write_access(retailer)

        supplier.is_active = True
        supplier.deleted_at = None

        supplier.save(
            update_fields=[
                "is_active",
                "deleted_at",
                "updated_at",
            ]
        )

        create_audit_log(
            user=user,
            action="activate",
            model_name="Supplier",
            object_id=supplier.id,
            description=f"Activated Supplier {supplier.name}",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Supplier activated successfully.",
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# HARD DELETE
# =========================================================


class SupplierDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    def delete(self, request, pk):

        user = request.user

        supplier = get_supplier_object(request, pk)

        retailer = get_supplier_retailer(user, request)

        if not user.is_superuser:
            check_subscription_write_access(retailer)

        supplier_id = supplier.id
        supplier_name = supplier.name

        try:
            with transaction.atomic():
                supplier.delete()

        except ProtectedError:
            raise ValidationError(
                {
                    "detail": "This supplier cannot be deleted because it is linked to existing records."
                }
            )

        create_audit_log(
            user=user,
            action="delete",
            model_name="Supplier",
            object_id=supplier_id,
            description=f"Permanently deleted Supplier {supplier_name}",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Supplier deleted permanently.",
            },
            status=status.HTTP_200_OK,
        )
