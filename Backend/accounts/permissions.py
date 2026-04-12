from rest_framework.permissions import BasePermission, SAFE_METHODS

# ================= HELPER FUNCTIONS ================= #

def is_admin(user):
    """Check if the user is an Admin or Superuser."""
    return (
        user.is_authenticated and
        (user.role == 'admin' or user.is_superuser)
    )


def is_staff(user):
    """Check if the user is Staff."""
    return (
        user.is_authenticated and
        user.role == 'staff'
    )


def has_role(user, roles):
    """Generic role checker."""
    return (
        user.is_authenticated and
        (user.role in roles or user.is_superuser)
    )


# ================= ADMIN PERMISSION ================= #

class IsAdmin(BasePermission):
    """
    Allows access only to Admins and Superusers.
    """
    message = "Only administrators have permission to perform this action."

    def has_permission(self, request, view):
        return is_admin(request.user)

# ================= SUPER ADMIN PERMISSION ================= #

class IsSuperAdmin(BasePermission):
    """
    Allows access only to Super Admins.
    """
    message = "Only the Super Admin can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.is_superuser
        )

# ================= STAFF PERMISSION ================= #

class IsStaff(BasePermission):
    """
    Allows access only to Staff members.
    """
    message = "Only staff members have permission to perform this action."

    def has_permission(self, request, view):
        return is_staff(request.user)


# ================= ADMIN OR STAFF ================= #

class IsAdminOrStaff(BasePermission):
    """
    Allows access to Admins, Staff, and Superusers.
    """
    message = "Only admin or staff members can access this resource."

    def has_permission(self, request, view):
        return has_role(request.user, ['admin', 'staff'])


# ================= OWNER OR ADMIN ================= #

class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission:
    - Owners can access their own data.
    - Admins and Superusers can access any data.
    """
    message = "You do not have permission to access this resource."

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Determine the owner field dynamically
        owner = getattr(obj, 'user', None) or getattr(obj, 'owner', None)

        # If object itself is a User instance
        if owner is None:
            owner = obj

        return is_admin(request.user) or owner == request.user


# ================= READ-ONLY PERMISSION ================= #

class ReadOnly(BasePermission):
    """
    Allows read-only access.
    """
    message = "This resource is read-only."

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


# ================= ADMIN OR READ-ONLY ================= #

class IsAdminOrReadOnly(BasePermission):
    """
    Allows read-only access to everyone and write access only to Admins.
    """
    message = "Only administrators can modify this resource."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            is_admin(request.user)
        )


# ================= PHARMACY-SPECIFIC PERMISSIONS ================= #

class IsPharmacist(BasePermission):
    """
    Allows access only to Pharmacists.
    """
    message = "Only pharmacists are allowed to perform this action."

    def has_permission(self, request, view):
        return has_role(request.user, ['pharmacist'])


class IsCashier(BasePermission):
    """
    Allows access only to Cashiers.
    """
    message = "Only cashiers are allowed to perform this action."

    def has_permission(self, request, view):
        return has_role(request.user, ['cashier'])


class IsStoreManager(BasePermission):
    """
    Allows access only to Store Managers.
    """
    message = "Only store managers are allowed to perform this action."

    def has_permission(self, request, view):
        return has_role(request.user, ['store_manager'])


class IsPharmacistOrAdmin(BasePermission):
    """
    Allows access to Pharmacists and Admins.
    """
    message = "Only pharmacists or administrators can perform this action."

    def has_permission(self, request, view):
        return has_role(request.user, ['admin', 'pharmacist'])


class IsManagerOrAdmin(BasePermission):
    """
    Allows access to Store Managers and Admins.
    """
    message = "Only store managers or administrators can perform this action."

    def has_permission(self, request, view):
        return has_role(request.user, ['admin', 'store_manager'])