class BranchFilterMixin:
    """
    Mixin to enforce branch-based data access.
    Super Admins can access all data, while other users
    are restricted to their assigned branch.
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Super Admin or Django Superuser can access all records
        if user.is_superuser or getattr(user, "role", None) == "superadmin":
            return queryset

        # Filter by branch if the model contains a branch field
        if hasattr(queryset.model, "branch"):
            return queryset.filter(branch=user.branch)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user

        # Automatically assign branch during creation
        if hasattr(serializer.Meta.model, "branch"):
            if user.is_superuser or getattr(user, "role", None) == "superadmin":
                serializer.save()
            else:
                serializer.save(branch=user.branch)
        else:
            serializer.save()