from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Branch
from .serializers import BranchSerializer

from accounts.models import Retailer
from accounts.permissions import IsRetailerOwnerOrPlatformOwner
from accounts.views import create_audit_log

from subscriptions.utils import (
    validate_branch_subscription,
    check_subscription_write_access,
)

# =========================================================
# COMMON BRANCH ACCESS
# =========================================================


def get_branch_for_user(user, pk=None):

    queryset = Branch.objects.select_related("retailer", "created_by", "deleted_by")

    if user.is_platform_owner():
        pass

    elif user.is_retailer_owner():
        queryset = queryset.filter(retailer=user.retailer)

    elif user.is_admin():
        queryset = queryset.filter(retailer=user.retailer, id=user.branch_id)

    else:
        raise PermissionDenied("You do not have permission to access branches.")

    if pk is not None:
        try:
            return queryset.get(pk=pk)
        except Branch.DoesNotExist:
            return None

    return queryset


def check_branch_write_access(retailer):

    validate_branch_subscription(retailer)
    check_subscription_write_access(retailer)


# =========================================================
# BRANCH CREATE VIEW
# =========================================================


class BranchCreateView(APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        user = request.user

        # PLATFORM OWNER
        if user.is_platform_owner():

            retailer_id = request.data.get("retailer")

            if not retailer_id:
                return Response(
                    {"success": False, "message": "Retailer ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                retailer = Retailer.objects.get(pk=retailer_id)

            except Retailer.DoesNotExist:
                return Response(
                    {"success": False, "message": "Retailer not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        # RETAILER OWNER
        elif user.is_retailer_owner():

            retailer = user.retailer

        else:
            raise PermissionDenied("You do not have permission to create a branch.")

        check_branch_write_access(retailer)

        serializer = BranchSerializer(data=request.data, context={"request": request})

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": "Branch creation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():

                branch = serializer.save(retailer=retailer, created_by=user)

        except IntegrityError:
            return Response(
                {
                    "success": False,
                    "message": "Branch could not be created because of a duplicate name or code. Please try again.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        create_audit_log(
            user=user,
            action="create",
            model_name="Branch",
            object_id=branch.id,
            description=f"Branch {branch.name} created",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Branch created successfully.",
                "data": BranchSerializer(branch, context={"request": request}).data,
            },
            status=status.HTTP_201_CREATED,
        )


# =========================================================
# BRANCH LIST VIEW
# =========================================================


class BranchListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        queryset = get_branch_for_user(request.user)

        queryset = queryset.filter(is_active=True, deleted_at__isnull=True).order_by(
            "name"
        )

        serializer = BranchSerializer(queryset, many=True, context={"request": request})

        return Response(
            {"success": True, "count": queryset.count(), "data": serializer.data},
            status=status.HTTP_200_OK,
        )


# =========================================================
# BRANCH DETAIL VIEW
# =========================================================


class BranchDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        branch = get_branch_for_user(request.user, pk)

        if branch is None or branch.deleted_at is not None:
            return Response(
                {"success": False, "message": "Branch not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BranchSerializer(branch, context={"request": request})

        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


# =========================================================
# BRANCH UPDATE VIEW
# =========================================================


class BranchUpdateView(APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, pk):

        return self._update(request, pk, partial=False)

    def patch(self, request, pk):

        return self._update(request, pk, partial=True)

    def _update(self, request, pk, partial=False):

        branch = get_branch_for_user(request.user, pk)

        if branch is None or branch.deleted_at is not None:
            return Response(
                {"success": False, "message": "Branch not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = request.user

        if not user.is_platform_owner():
            check_branch_write_access(branch.retailer)

        serializer = BranchSerializer(
            branch, data=request.data, partial=partial, context={"request": request}
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": "Branch update failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():

                branch = serializer.save(
                    retailer=branch.retailer, created_by=branch.created_by
                )

        except IntegrityError:
            return Response(
                {
                    "success": False,
                    "message": "A branch with this name or code already exists.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        create_audit_log(
            user=user,
            action="update",
            model_name="Branch",
            object_id=branch.id,
            description=f"Branch {branch.name} updated",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Branch updated successfully.",
                "data": BranchSerializer(branch, context={"request": request}).data,
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# BRANCH SOFT DELETE VIEW
# =========================================================


class BranchSoftDeleteView(APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    def patch(self, request, pk):

        branch = get_branch_for_user(request.user, pk)

        if branch is None or branch.deleted_at is not None:
            return Response(
                {"success": False, "message": "Branch not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = request.user

        if not user.is_platform_owner():
            check_branch_write_access(branch.retailer)

        if not branch.is_active:
            return Response(
                {"success": False, "message": "Branch is already inactive."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        branch.soft_delete(user)

        create_audit_log(
            user=user,
            action="update",
            model_name="Branch",
            object_id=branch.id,
            description=f"Branch {branch.name} soft deleted",
            request=request,
        )

        return Response(
            {"success": True, "message": "Branch deactivated successfully."},
            status=status.HTTP_200_OK,
        )


# =========================================================
# BRANCH RESTORE VIEW
# =========================================================


class BranchRestoreView(APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    def patch(self, request, pk):

        branch = get_branch_for_user(request.user, pk)

        if branch is None:
            return Response(
                {"success": False, "message": "Branch not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = request.user

        if branch.deleted_at is None:
            return Response(
                {"success": False, "message": "Branch is not deleted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_platform_owner():
            check_branch_write_access(branch.retailer)

        try:
            with transaction.atomic():
                branch.restore()

        except IntegrityError:
            return Response(
                {
                    "success": False,
                    "message": "Cannot restore this branch. Another active branch already uses the same name or code.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        create_audit_log(
            user=user,
            action="update",
            model_name="Branch",
            object_id=branch.id,
            description=f"Branch {branch.name} restored",
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Branch restored successfully.",
                "data": BranchSerializer(branch, context={"request": request}).data,
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# BRANCH HARD DELETE VIEW
# =========================================================


class BranchHardDeleteView(APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    def delete(self, request, pk):

        branch = get_branch_for_user(request.user, pk)

        if branch is None:
            return Response(
                {"success": False, "message": "Branch not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = request.user

        if not user.is_platform_owner():
            check_branch_write_access(branch.retailer)

        branch_name = branch.name
        branch_id = branch.id

        try:
            with transaction.atomic():
                branch.hard_delete()

        except ProtectedError:
            return Response(
                {
                    "success": False,
                    "message": "This branch cannot be permanently deleted because it is linked to existing business records.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        create_audit_log(
            user=user,
            action="delete",
            model_name="Branch",
            object_id=branch_id,
            description=f"Branch {branch_name} permanently deleted",
            request=request,
        )

        return Response(
            {"success": True, "message": "Branch permanently deleted."},
            status=status.HTTP_200_OK,
        )


# =========================================================
# BRANCH STATUS FILTER VIEW
# =========================================================


class BranchStatusFilterView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        status_param = request.query_params.get("status", "active").lower()

        allowed_statuses = ["active", "inactive", "deleted", "all"]

        if status_param not in allowed_statuses:
            return Response(
                {
                    "success": False,
                    "message": "Invalid status. Use active, inactive, deleted or all.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = get_branch_for_user(request.user)

        if status_param == "active":

            queryset = queryset.filter(is_active=True, deleted_at__isnull=True)

        elif status_param == "inactive":

            queryset = queryset.filter(is_active=False, deleted_at__isnull=True)

        elif status_param == "deleted":

            queryset = queryset.filter(deleted_at__isnull=False)

        # all returns active, inactive and deleted branches.

        queryset = queryset.order_by("name")

        serializer = BranchSerializer(queryset, many=True, context={"request": request})

        return Response(
            {
                "success": True,
                "status": status_param,
                "count": queryset.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
