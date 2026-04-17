from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Branch
from .serializers import BranchSerializer
from accounts.permissions import IsSuperAdmin


# ================= CREATE BRANCH ================= #
class BranchCreateView(generics.CreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "success": True,
            "message": "Branch created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


# ================= LIST BRANCHES ================= #
class BranchListView(generics.ListAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Branch.objects.filter(is_active=True)

        if getattr(user, "branch", None):
            return Branch.objects.filter(
                id=user.branch.id,
                is_active=True
            )

        return Branch.objects.none()


# ================= BRANCH DETAIL ================= #
class BranchDetailView(generics.RetrieveAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]
    queryset = Branch.objects.all()

    def get_object(self):
        branch = super().get_object()
        user = self.request.user

        if user.is_superuser or getattr(user, "branch", None) == branch:
            return branch

        raise PermissionDenied("You do not have permission to access this branch.")


# ================= UPDATE BRANCH ================= #
class BranchUpdateView(generics.UpdateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

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
            "message": "Branch updated successfully",
            "data": serializer.data
        })


# ================= SOFT DELETE ================= #
class BranchSoftDeleteView(generics.UpdateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def patch(self, request, *args, **kwargs):
        branch = self.get_object()

        if not branch.is_active:
            return Response({
                "success": False,
                "message": "Branch already deactivated"
            }, status=400)

        branch.soft_delete(request.user)

        return Response({
            "success": True,
            "message": "Branch deactivated successfully"
        })


# ================= RESTORE ================= #
class BranchRestoreView(generics.UpdateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def patch(self, request, *args, **kwargs):
        branch = self.get_object()

        if branch.is_active:
            return Response({
                "success": False,
                "message": "Branch already active"
            }, status=400)

        branch.restore()

        return Response({
            "success": True,
            "message": "Branch restored successfully"
        })

# ================= HARD DELETE ================= #
class BranchHardDeleteView(generics.DestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def destroy(self, request, *args, **kwargs):
        branch = self.get_object()
        branch.hard_delete()

        return Response({
            "success": True,
            "message": "Branch permanently deleted"
        }, status=status.HTTP_200_OK)


# ================= FILTER BRANCH (ACTIVE / INACTIVE) ================= #
class BranchStatusFilterView(generics.ListAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get_queryset(self):
        status_param = self.request.query_params.get("status", "active").lower()

        if status_param == "active":
            return Branch.objects.filter(is_active=True)

        elif status_param == "inactive":
            return Branch.objects.filter(is_active=False)

        elif status_param == "all":
            return Branch.objects.all()

        return Branch.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "success": True,
            "message": "Branch filtered successfully",
            "count": queryset.count(),
            "data": serializer.data
        })