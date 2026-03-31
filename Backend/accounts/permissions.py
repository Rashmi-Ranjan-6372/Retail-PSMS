from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'admin'
        )

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'staff'
        )

class IsAdminOrStaff(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in ['admin', 'staff']
        )

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            (
                request.user.role == 'admin' or
                obj == request.user
            )
        )

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET']

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in ['GET'] or
            (
                request.user.is_authenticated and
                request.user.role == 'admin'
            )
        )