from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Branch
from .serializers import BranchSerializer
from accounts.permissions import IsSuperAdmin


# ================= CREATE BRANCH ================= #
class BranchCreateView(generics.CreateAPIView):
    """
    Create a new branch.
    Accessible only by Super Admin.
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                "success": True,
                "message": "Branch created successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


# ================= LIST BRANCHES ================= #
class BranchListView(generics.ListAPIView):
    """
    List branches:
    - Super Admin: View all branches
    - Other Users: View only their assigned branch
    """
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Branch.objects.all()

        if hasattr(user, "branch") and user.branch:
            return Branch.objects.filter(id=user.branch.id)

        return Branch.objects.none()


# ================= BRANCH DETAIL ================= #
class BranchDetailView(generics.RetrieveAPIView):
    """
    Retrieve details of a specific branch.
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        branch = super().get_object()
        user = self.request.user

        if user.is_superuser or getattr(user, "branch", None) == branch:
            return branch

        raise PermissionDenied("You do not have permission to access this branch.")


# ================= UPDATE BRANCH ================= #
class BranchUpdateView(generics.UpdateAPIView):
    """
    Update branch details.
    Accessible only by Super Admin.
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "success": True,
                "message": "Branch updated successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ================= DELETE BRANCH ================= #
class BranchDeleteView(generics.DestroyAPIView):
    """
    Delete a branch.
    Accessible only by Super Admin.
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {
                "success": True,
                "message": "Branch deleted successfully",
            },
            status=status.HTTP_200_OK,
        )