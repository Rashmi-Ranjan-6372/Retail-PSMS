from rest_framework.permissions import BasePermission

def is_super_admin(user):
    return (
        user.is_authenticated and
        (getattr(user, "role", None) == "superadmin" or user.is_superuser)
    )


class IsSuperAdmin(BasePermission):
    message = "Only the Super Admin can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )


class IsBranchAdmin(BasePermission):
    message = "Only branch administrators have permission."
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and
            getattr(user, "role", None) == "admin"
        )

class IsSameBranch(BasePermission):
    message = "You can only access records from your assigned branch."

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if is_super_admin(user):
            return True

        if hasattr(obj, "branch"):
            return obj.branch == user.branch

        return False