from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Branch
from .serializers import BranchSerializer
from accounts.permissions import IsSuperAdmin, is_super_admin
from accounts.views import create_audit_log


# ==================== BRANCH CREATE VIEW ==================== #

class BranchCreateView(generics.CreateAPIView):
    queryset = Branch.objects.select_related("retailer")
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        branch = serializer.save(retailer=self.request.user.retailer)

        create_audit_log(
            user=self.request.user,
            action="create",
            model_name="Branch",
            object_id=branch.id,
            description=f"Branch {branch.name} created",
            request=self.request
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return Response({
            "success": True,
            "message": "Branch created successfully",
            "data": response.data
        }, status=status.HTTP_201_CREATED)


# ==================== BRANCH LIST VIEW ==================== #

class BranchListView(generics.ListAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # PLATFORM OWNER
        if is_super_admin(user):
            return Branch.objects.filter(
                deleted_at__isnull=True
            ).select_related("retailer")

        # RETAILER OWNER
        if user.role == "superadmin":
            return Branch.objects.filter(
                retailer=user.retailer,
                deleted_at__isnull=True
            )

        # ADMIN (branch level)
        if user.role == "admin":
            return Branch.objects.filter(
                id=user.branch_id,
                retailer=user.retailer,
                deleted_at__isnull=True
            )

        return Branch.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        })

# ==================== BRANCH DETAIL VIEW ==================== #

class BranchDetailView(generics.RetrieveAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

    queryset = Branch.objects.filter(
        deleted_at__isnull=True
    ).select_related("retailer")

    def get_object(self):
        branch = super().get_object()
        user = self.request.user

        if is_super_admin(user):
            return branch

        if user.role == "superadmin" and branch.retailer == user.retailer:
            return branch

        if user.role == "admin" and branch.id == user.branch_id:
            return branch

        raise PermissionDenied("You do not have access to this branch")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            "success": True,
            "data": serializer.data
        })


# ==================== BRANCH UPDATE VIEW ==================== #

class BranchUpdateView(generics.UpdateAPIView):
    queryset = Branch.objects.filter(deleted_at__isnull=True)
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        branch = super().get_object()
        user = self.request.user

        if is_super_admin(user):
            return branch

        if branch.retailer != user.retailer:
            raise PermissionDenied("Not allowed")

        return branch

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        create_audit_log(
            user=request.user,
            action="update",
            model_name="Branch",
            object_id=kwargs.get("pk"),
            description="Branch updated",
            request=request
        )

        return Response({
            "success": True,
            "message": "Branch updated successfully",
            "data": response.data
        })


# ==================== BRANCH SOFT DELETE VIEW ==================== #

class BranchSoftDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def patch(self, request, pk):
        try:
            branch = Branch.objects.get(pk=pk, deleted_at__isnull=True)
        except Branch.DoesNotExist:
            return Response({
                "success": False,
                "message": "Branch not found"
            }, status=404)

        user = request.user

        if not is_super_admin(user) and branch.retailer != user.retailer:
            raise PermissionDenied("Not allowed")

        if not branch.is_active:
            return Response({
                "success": False,
                "message": "Branch already inactive"
            }, status=400)

        branch.soft_delete(user)

        create_audit_log(
            user=user,
            action="update",
            model_name="Branch",
            object_id=branch.id,
            description="Branch soft deleted",
            request=request
        )

        return Response({
            "success": True,
            "message": "Branch deactivated successfully"
        })


# ==================== BRANCH RESTORE VIEW ==================== #

class BranchRestoreView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def patch(self, request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        user = request.user

        if not is_super_admin(user) and branch.retailer != user.retailer:
            raise PermissionDenied("Not allowed")

        if branch.is_active:
            return Response({
                "success": False,
                "message": "Branch already active"
            }, status=400)

        branch.restore()

        create_audit_log(
            user=user,
            action="update",
            model_name="Branch",
            object_id=branch.id,
            description="Branch restored",
            request=request
        )

        return Response({
            "success": True,
            "message": "Branch restored successfully"
        })


# ==================== BRANCH HARD DELETE VIEW ==================== #

class BranchHardDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def delete(self, request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        user = request.user

        if not is_super_admin(user) and branch.retailer != user.retailer:
            raise PermissionDenied("Not allowed")

        branch_name = branch.name
        branch.hard_delete()

        create_audit_log(
            user=user,
            action="delete",
            model_name="Branch",
            object_id=pk,
            description=f"Branch {branch_name} permanently deleted",
            request=request
        )

        return Response({
            "success": True,
            "message": "Branch permanently deleted"
        })


# ==================== BRANCH STATUS FILTER VIEW ==================== #

class BranchStatusFilterView(generics.ListAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status_param = self.request.query_params.get("status", "active")

        queryset = Branch.objects.select_related("retailer")

        if status_param == "active":
            return queryset.filter(is_active=True, deleted_at__isnull=True)

        if status_param == "inactive":
            return queryset.filter(is_active=False)

        if status_param == "all":
            return queryset.all()

        return queryset.filter(is_active=True, deleted_at__isnull=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        })