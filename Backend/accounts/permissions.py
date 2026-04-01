from rest_framework.permissions import BasePermission


# ================= HELPER FUNCTION ================= #
def is_admin(user):
    return (
        user.is_authenticated and
        (user.role == 'admin' or user.is_superuser)
    )

# ================= ADMIN ================= #
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return is_admin(request.user)

# ================= STAFF ================= #
class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'staff'
        )

# ================= ADMIN OR STAFF ================= #
class IsAdminOrStaff(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (
                request.user.role in ['admin', 'staff'] or
                request.user.is_superuser
            )
        )

# ================= OWNER OR ADMIN ================= #
class IsOwnerOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated 

    def has_object_permission(self, request, view, obj):
        return (
            is_admin(request.user) or
            obj == request.user
        )

# ================= READ ONLY ================= #
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET']

# ================= ADMIN OR READ ONLY ================= #
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in ['GET'] or
            is_admin(request.user)
        )