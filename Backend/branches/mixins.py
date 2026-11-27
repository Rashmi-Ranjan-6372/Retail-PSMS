from rest_framework.exceptions import PermissionDenied


class BranchFilterMixin:
    """
    Retailer and branch level data isolation.

    Platform Owner:
        Can access all retailers and branches.

    Super Admin:
        Can access all branches within their retailer.

    Other users:
        Can access only their assigned active branch.
    """

    # =====================================================
    # ROLE CHECKS
    # =====================================================

    def is_platform_owner(self):

        user = self.request.user

        return (
            user.is_authenticated
            and user.is_active
            and (user.is_superuser or getattr(user, "role", None) == "platform_owner")
        )

    def is_super_admin(self):

        user = self.request.user

        return (
            user.is_authenticated
            and user.is_active
            and getattr(user, "role", None) == "superadmin"
            and user.retailer_id is not None
        )

    # =====================================================
    # MODEL FIELD CHECK
    # =====================================================

    @staticmethod
    def model_has_field(model, field_name):

        try:
            model._meta.get_field(field_name)
            return True

        except Exception:
            return False

    # =====================================================
    # BRANCH VALIDATION
    # =====================================================

    def is_valid_user_branch(self, user, branch):

        return (
            branch is not None
            and branch.retailer_id == user.retailer_id
            and branch.is_active
            and branch.deleted_at is None
        )

    # =====================================================
    # QUERYSET FILTERING
    # =====================================================

    def filter_queryset_by_user(self, queryset):

        user = self.request.user

        if self.is_platform_owner():
            return queryset

        if not user.retailer_id:
            return queryset.none()

        model = queryset.model

        if self.model_has_field(model, "retailer"):

            queryset = queryset.filter(retailer_id=user.retailer_id)

        if self.is_super_admin():
            return queryset

        if not self.model_has_field(model, "branch"):
            return queryset

        branch = getattr(user, "branch", None)

        if not self.is_valid_user_branch(user, branch):
            return queryset.none()

        return queryset.filter(branch_id=branch.id)

    # =====================================================
    # GENERIC VIEW QUERYSET
    # =====================================================

    def get_queryset(self):

        queryset = super().get_queryset()

        return self.filter_queryset_by_user(queryset)

    # =====================================================
    # CREATE OBJECT
    # =====================================================

    def perform_create(self, serializer):

        user = self.request.user

        if self.is_platform_owner():

            serializer.save()
            return

        if not user.retailer_id:

            raise PermissionDenied("You are not associated with any retailer.")

        model = serializer.Meta.model

        save_kwargs = {}

        if self.model_has_field(model, "retailer"):

            save_kwargs["retailer"] = user.retailer

        if self.model_has_field(model, "branch"):

            if self.is_super_admin():

                branch = serializer.validated_data.get("branch")

                if not self.is_valid_user_branch(user, branch):

                    raise PermissionDenied(
                        "Please select a valid active branch "
                        "belonging to your retailer."
                    )

                save_kwargs["branch"] = branch

            else:

                branch = getattr(user, "branch", None)

                if not self.is_valid_user_branch(user, branch):

                    raise PermissionDenied("You are not assigned to an active branch.")

                save_kwargs["branch"] = branch

        serializer.save(**save_kwargs)
