from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Branch
from .serializers import BranchSerializer

from accounts.permissions import IsRetailerOwnerOrPlatformOwner
from accounts.views import create_audit_log

from subscriptions.utils import (
    validate_branch_subscription,
    check_subscription_write_access,
)

# =========================================================
# BRANCH CREATE VIEW
# =========================================================


class BranchCreateView(APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        user = request.user
        retailer = user.retailer

        validate_branch_subscription(retailer)
        check_subscription_write_access(retailer)

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

        branch = serializer.save(retailer=retailer, created_by=user)

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

        user = request.user

        # PLATFORM OWNER
        if user.is_platform_owner():

            queryset = Branch.objects.filter(deleted_at__isnull=True).select_related(
                "retailer", "created_by", "deleted_by"
            )

        # RETAILER OWNER
        elif user.is_retailer_owner():

            queryset = Branch.objects.filter(
                retailer=user.retailer, deleted_at__isnull=True
            ).select_related("retailer", "created_by", "deleted_by")

        # ADMIN
        elif user.is_admin():

            queryset = Branch.objects.filter(
                id=user.branch_id, retailer=user.retailer, deleted_at__isnull=True
            ).select_related("retailer", "created_by", "deleted_by")

        else:

            queryset = Branch.objects.none()

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

        try:

            branch = Branch.objects.select_related(
                "retailer", "created_by", "deleted_by"
            ).get(pk=pk, deleted_at__isnull=True)

        except Branch.DoesNotExist:

            return Response(
                {"success": False, "message": "Branch not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = request.user

        # PLATFORM OWNER
        if user.is_platform_owner():

            pass

        # RETAILER OWNER
        elif user.is_retailer_owner():

            if branch.retailer != user.retailer:

                raise PermissionDenied("You do not have access to this branch.")

        # ADMIN
        elif user.is_admin():

            if branch.id != user.branch_id or branch.retailer != user.retailer:

                raise PermissionDenied("You do not have access to this branch.")

        else:

            raise PermissionDenied("You do not have access to this branch.")

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

        try:

            branch = Branch.objects.select_related(
                "retailer", "created_by", "deleted_by"
            ).get(pk=pk, deleted_at__isnull=True)

        except Branch.DoesNotExist:

            return Response(
                {"success": False, "message": "Branch not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = request.user

        # PLATFORM OWNER
        if user.is_platform_owner():

            pass

        # RETAILER OWNER
        elif user.is_retailer_owner():

            if branch.retailer != user.retailer:

                raise PermissionDenied("You do not have access to this branch.")

        else:

            raise PermissionDenied("You do not have permission to update this branch.")

        if not user.is_platform_owner():

            validate_branch_subscription(user.retailer)

            check_subscription_write_access(user.retailer)

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

        branch = serializer.save(retailer=branch.retailer, created_by=branch.created_by)

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

        try:

            branch = Branch.objects.select_related("retailer").get(
                pk=pk, deleted_at__isnull=True
            )

        except Branch.DoesNotExist:

            return Response(
                {"success": False, "message": "Branch not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = request.user

        # PLATFORM OWNER
        if user.is_platform_owner():

            pass

        # RETAILER OWNER
        elif user.is_retailer_owner():

            if branch.retailer != user.retailer:

                raise PermissionDenied("You do not have access to this branch.")

        else:

            raise PermissionDenied("You do not have permission to delete this branch.")

        if not branch.is_active:

            return Response(
                {"success": False, "message": "Branch already inactive."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_platform_owner():

            validate_branch_subscription(user.retailer)

            check_subscription_write_access(user.retailer)

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

        try:

            branch = Branch.objects.select_related("retailer").get(pk=pk)

        except Branch.DoesNotExist:

            return Response(
                {"success": False, "message": "Branch not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = request.user

        # PLATFORM OWNER
        if user.is_platform_owner():

            pass

        # RETAILER OWNER
        elif user.is_retailer_owner():

            if branch.retailer != user.retailer:

                raise PermissionDenied("You do not have access to this branch.")

        else:

            raise PermissionDenied("You do not have permission to restore this branch.")

        if branch.is_active:

            return Response(
                {"success": False, "message": "Branch already active."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_platform_owner():

            validate_branch_subscription(branch.retailer)

            check_subscription_write_access(branch.retailer)

        branch.restore()

        create_audit_log(
            user=user,
            action="update",
            model_name="Branch",
            object_id=branch.id,
            description=f"Branch {branch.name} restored",
            request=request,
        )

        return Response(
            {"success": True, "message": "Branch restored successfully."},
            status=status.HTTP_200_OK,
        )


# =========================================================
# BRANCH HARD DELETE VIEW
# =========================================================


class BranchHardDeleteView(APIView):

    permission_classes = [IsAuthenticated, IsRetailerOwnerOrPlatformOwner]

    def delete(self, request, pk):

        try:

            branch = Branch.objects.select_related("retailer").get(pk=pk)

        except Branch.DoesNotExist:

            return Response(
                {"success": False, "message": "Branch not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = request.user

        # PLATFORM OWNER
        if user.is_platform_owner():

            pass

        # RETAILER OWNER
        elif user.is_retailer_owner():

            if branch.retailer != user.retailer:

                raise PermissionDenied("You do not have access to this branch.")

        else:

            raise PermissionDenied(
                "You do not have permission to permanently delete this branch."
            )

        if not user.is_platform_owner():

            validate_branch_subscription(user.retailer)

            check_subscription_write_access(user.retailer)

        branch_name = branch.name
        branch_id = branch.id

        branch.hard_delete()

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

        user = request.user

        status_param = request.query_params.get("status", "active").lower()

        queryset = Branch.objects.select_related("retailer", "created_by", "deleted_by")

        # PLATFORM OWNER
        if user.is_platform_owner():

            pass

        # RETAILER OWNER
        elif user.is_retailer_owner():

            queryset = queryset.filter(retailer=user.retailer)

        # ADMIN
        elif user.is_admin():

            queryset = queryset.filter(id=user.branch_id, retailer=user.retailer)

        else:

            queryset = Branch.objects.none()

        if status_param == "active":

            queryset = queryset.filter(is_active=True, deleted_at__isnull=True)

        elif status_param == "inactive":

            queryset = queryset.filter(is_active=False)

        elif status_param == "all":

            pass

        else:

            queryset = queryset.filter(is_active=True, deleted_at__isnull=True)

        serializer = BranchSerializer(queryset, many=True, context={"request": request})

        return Response(
            {"success": True, "count": queryset.count(), "data": serializer.data},
            status=status.HTTP_200_OK,
        )
