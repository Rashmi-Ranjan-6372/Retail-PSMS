from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Branch
from .serializers import BranchSerializer
from accounts.permissions import IsSuperAdmin, is_super_admin


# ==================== BRANCH CREATE VIEW ==================== #

class BranchCreateView(generics.CreateAPIView):
    queryset = Branch.objects.select_related("retailer")
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(retailer=self.request.user.retailer)

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

        if is_super_admin(user):
            return Branch.objects.filter(
                is_active=True,
                deleted_at__isnull=True
            ).select_related("retailer")

        if getattr(user, "branch", None):
            return Branch.objects.filter(
                id=user.branch.id,
                retailer=user.retailer,
                is_active=True,
                deleted_at__isnull=True
            ).select_related("retailer")

        return Branch.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True,
            context={"request": request}
        )

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

        if (
            getattr(user, "branch", None) == branch and
            getattr(user, "retailer", None) == branch.retailer
        ):
            return branch

        raise PermissionDenied(
            "You do not have permission to access this branch."
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            context={"request": request}
        )

        return Response({
            "success": True,
            "data": serializer.data
        })


# ==================== BRANCH UPDATE VIEW ==================== #

class BranchUpdateView(generics.UpdateAPIView):
    queryset = Branch.objects.filter(
        deleted_at__isnull=True
    ).select_related("retailer")

    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        branch = super().get_object()
        user = self.request.user

        if is_super_admin(user):
            return branch

        if branch.retailer != user.retailer:
            raise PermissionDenied(
                "You cannot access another retailer branch."
            )

        return branch

    def perform_update(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        return Response({
            "success": True,
            "message": "Branch updated successfully",
            "data": response.data
        })


# ==================== BRANCH SOFT DELETE VIEW ==================== #

class BranchSoftDeleteView(generics.UpdateAPIView):
    queryset = Branch.objects.filter(
        deleted_at__isnull=True
    ).select_related("retailer")

    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get_object(self):
        branch = super().get_object()
        user = self.request.user

        if is_super_admin(user):
            return branch

        if branch.retailer != user.retailer:
            raise PermissionDenied(
                "You cannot access another retailer branch."
            )

        return branch

    def patch(self, request, *args, **kwargs):
        branch = self.get_object()

        if not branch.is_active:
            return Response({
                "success": False,
                "message": "Branch already deactivated"
            }, status=status.HTTP_400_BAD_REQUEST)

        branch.soft_delete(request.user)

        return Response({
            "success": True,
            "message": "Branch deactivated successfully"
        })


# ==================== BRANCH RESTORE VIEW ==================== #

class BranchRestoreView(generics.UpdateAPIView):
    queryset = Branch.objects.select_related("retailer")
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get_object(self):
        branch = super().get_object()
        user = self.request.user

        if is_super_admin(user):
            return branch

        if branch.retailer != user.retailer:
            raise PermissionDenied(
                "You cannot access another retailer branch."
            )

        return branch

    def patch(self, request, *args, **kwargs):
        branch = self.get_object()

        if branch.is_active:
            return Response({
                "success": False,
                "message": "Branch already active"
            }, status=status.HTTP_400_BAD_REQUEST)

        branch.restore()

        return Response({
            "success": True,
            "message": "Branch restored successfully"
        })


# ==================== BRANCH HARD DELETE VIEW ==================== #

class BranchHardDeleteView(generics.DestroyAPIView):
    queryset = Branch.objects.select_related("retailer")
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get_object(self):
        branch = super().get_object()
        user = self.request.user

        if is_super_admin(user):
            return branch

        if branch.retailer != user.retailer:
            raise PermissionDenied(
                "You cannot access another retailer branch."
            )

        return branch

    def destroy(self, request, *args, **kwargs):
        branch = self.get_object()

        branch.hard_delete()

        return Response({
            "success": True,
            "message": "Branch permanently deleted"
        }, status=status.HTTP_200_OK)


# ==================== BRANCH STATUS FILTER VIEW ==================== #

class BranchStatusFilterView(generics.ListAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get_queryset(self):
        status_param = self.request.query_params.get(
            "status",
            "active"
        ).lower()

        queryset = Branch.objects.select_related(
            "retailer"
        )

        if status_param == "active":
            return queryset.filter(
                is_active=True,
                deleted_at__isnull=True
            )

        elif status_param == "inactive":
            return queryset.filter(
                is_active=False
            )

        elif status_param == "all":
            return queryset.all()

        return queryset.filter(
            is_active=True,
            deleted_at__isnull=True
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True,
            context={"request": request}
        )

        return Response({
            "success": True,
            "message": "Branch filtered successfully",
            "count": queryset.count(),
            "data": serializer.data
        })