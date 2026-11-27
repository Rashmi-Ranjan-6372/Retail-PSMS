from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS
)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def is_platform_owner(user):
    return (
        user.is_authenticated
        and user.is_active
        and user.is_superuser
    )


def is_retailer_owner(user):
    return (
        user.is_authenticated
        and user.is_active
        and getattr(user, "role", None) == "superadmin"
        and user.retailer_id is not None
    )


def is_admin(user):
    return (
        user.is_authenticated
        and user.is_active
        and (
            getattr(user, "role", None) == "admin"
            or is_retailer_owner(user)
            or is_platform_owner(user)
        )
    )


def is_store_manager(user):
    return (
        user.is_authenticated
        and user.is_active
        and getattr(user, "role", None) == "store_manager"
    )


def is_pharmacist(user):
    return (
        user.is_authenticated
        and user.is_active
        and getattr(user, "role", None) == "pharmacist"
    )


def is_cashier(user):
    return (
        user.is_authenticated
        and user.is_active
        and getattr(user, "role", None) == "cashier"
    )


def is_staff_member(user):
    return (
        user.is_authenticated
        and user.is_active
        and getattr(user, "role", None) == "staff"
    )


def has_role(user, roles, allow_higher_roles=True):

    if not (
        user.is_authenticated
        and user.is_active
    ):
        return False

    if getattr(user, "role", None) in roles:
        return True

    if allow_higher_roles:
        return (
            is_retailer_owner(user)
            or is_platform_owner(user)
        )

    return False


# =====================================================
# PLATFORM OWNER
# =====================================================

class IsPlatformOwner(BasePermission):

    message = "Only Platform Owner can perform this action."

    def has_permission(self, request, view):
        return is_platform_owner(request.user)


# =====================================================
# RETAILER OWNER
# =====================================================

class IsRetailerOwner(BasePermission):

    message = "Only Retailer Owner can perform this action."

    def has_permission(self, request, view):
        return is_retailer_owner(request.user)


# =====================================================
# RETAILER OWNER OR PLATFORM OWNER
# =====================================================

class IsRetailerOwnerOrPlatformOwner(BasePermission):

    message = (
        "Only Platform Owner or Retailer Owner "
        "can perform this action."
    )

    def has_permission(self, request, view):

        user = request.user

        return (
            user.is_authenticated and
            user.is_active and
            (
                is_platform_owner(user) or
                is_retailer_owner(user)
            )
        )


# =====================================================
# ADMIN
# =====================================================

class IsAdmin(BasePermission):

    message = "Only administrators have permission."

    def has_permission(self, request, view):
        return is_admin(request.user)


# =====================================================
# STAFF
# =====================================================

class IsStaff(BasePermission):

    message = "Only staff members have permission."

    def has_permission(self, request, view):
        return is_staff_member(request.user)


# =====================================================
# ADMIN OR STAFF
# =====================================================

class IsAdminOrStaff(BasePermission):

    message = "Only admin or staff can access this resource."

    def has_permission(self, request, view):
        return has_role(
            request.user,
            ["admin", "staff"]
        )


# =====================================================
# OWNER OR ADMIN
# =====================================================

class IsOwnerOrAdmin(BasePermission):

    message = (
        "You do not have permission "
        "to access this resource."
    )

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.is_active
        )

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):

        owner = (
            getattr(obj, "user", None) or
            getattr(obj, "owner", None)
        )

        if owner is None:
            owner = obj

        return (
            is_admin(request.user) or
            owner == request.user
        )


# =====================================================
# READ ONLY
# =====================================================

class ReadOnly(BasePermission):

    message = "This resource is read-only."

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


# =====================================================
# ADMIN OR READ ONLY
# =====================================================

class IsAdminOrReadOnly(BasePermission):

    message = (
        "Only administrators can modify "
        "this resource."
    )

    def has_permission(self, request, view):

        return (
            request.method in SAFE_METHODS or
            is_admin(request.user)
        )


# =====================================================
# SAME RETAILER
# =====================================================

class IsSameRetailer(BasePermission):

    message = "You can only access your retailer data."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
        )

    def has_object_permission(self, request, view, obj):

        user = request.user

        if is_platform_owner(user):
            return True

        if not user.retailer_id:
            return False

        retailer_id = getattr(obj, "retailer_id", None)

        return retailer_id == user.retailer_id


# =====================================================
# SAME BRANCH
# =====================================================

class IsSameBranch(BasePermission):

    message = "You can only access your branch data."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
        )

    def has_object_permission(self, request, view, obj):

        user = request.user

        if is_platform_owner(user):
            return True

        if not user.retailer_id:
            return False

        # Super Admin: all branches within their retailer
        if is_retailer_owner(user):

            obj_retailer_id = getattr(
                obj,
                "retailer_id",
                None
            )

            return obj_retailer_id == user.retailer_id

        # Other users: only their assigned branch
        if not user.branch_id:
            return False

        obj_branch_id = getattr(
            obj,
            "branch_id",
            None
        )

        return (
            obj_branch_id == user.branch_id
            and user.branch.retailer_id == user.retailer_id
        )


# =====================================================
# SAME RETAILER AND BRANCH
# =====================================================

class IsSameRetailerAndBranch(BasePermission):

    message = (
        "You can only access records from your "
        "retailer and branch."
    )

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
        )

    def has_object_permission(self, request, view, obj):

        user = request.user

        # Platform Owner: global access
        if is_platform_owner(user):
            return True

        # Retailer must be assigned
        if not user.retailer_id:
            return False

        # Object must have retailer field
        obj_retailer_id = getattr(
            obj,
            "retailer_id",
            None
        )

        if obj_retailer_id != user.retailer_id:
            return False

        # Super Admin: all branches of their retailer
        if is_retailer_owner(user):
            return True

        # Other users must have an assigned branch
        if not user.branch_id:
            return False

        # User's branch must belong to their retailer
        if user.branch.retailer_id != user.retailer_id:
            return False

        obj_branch_id = getattr(
            obj,
            "branch_id",
            None
        )

        return obj_branch_id == user.branch_id


# =====================================================
# PHARMACIST
# =====================================================

class IsPharmacist(BasePermission):

    message = "Only pharmacists are allowed."

    def has_permission(self, request, view):

        return has_role(
            request.user,
            ["pharmacist"]
        )


# =====================================================
# CASHIER
# =====================================================

class IsCashier(BasePermission):

    message = "Only cashiers are allowed."

    def has_permission(self, request, view):

        return has_role(
            request.user,
            ["cashier"]
        )


# =====================================================
# STORE MANAGER
# =====================================================

class IsStoreManager(BasePermission):

    message = "Only store managers are allowed."

    def has_permission(self, request, view):

        return has_role(
            request.user,
            ["store_manager"]
        )


# =====================================================
# PHARMACIST OR ADMIN
# =====================================================

class IsPharmacistOrAdmin(BasePermission):

    message = (
        "Only pharmacists or admins "
        "can perform this action."
    )

    def has_permission(self, request, view):

        return has_role(
            request.user,
            ["admin", "pharmacist"]
        )


# =====================================================
# MANAGER OR ADMIN
# =====================================================

class IsManagerOrAdmin(BasePermission):

    message = (
        "Only store managers or admins "
        "can perform this action."
    )

    def has_permission(self, request, view):

        return has_role(
            request.user,
            ["admin", "store_manager"]
        )


# =====================================================
# ADMIN / MANAGER / PHARMACIST
# =====================================================

class IsAdminManagerOrPharmacist(BasePermission):

    message = (
        "Only admin, manager, or pharmacist "
        "can perform this action."
    )

    def has_permission(self, request, view):

        return has_role(
            request.user,
            [
                "admin",
                "store_manager",
                "pharmacist"
            ]
        )


# =====================================================
# ADMIN / CASHIER
# =====================================================

class IsAdminOrCashier(BasePermission):

    message = (
        "Only admin or cashier "
        "can perform this action."
    )

    def has_permission(self, request, view):

        return has_role(
            request.user,
            [
                "admin",
                "cashier"
            ]
        )