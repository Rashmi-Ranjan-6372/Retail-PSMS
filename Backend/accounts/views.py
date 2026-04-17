from branches.models import Branch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.db.models import Q
from django.utils import timezone

from .serializers import (
    AdminResetPasswordSerializer,
    LoginSerializer,
    UserSerializer,
    CreateStaffSerializer
)
from .permissions import IsAdmin
from .models import LoginLog, UserSession

User = get_user_model()


# ================= HELPER FUNCTIONS ================= #

def get_client_ip(request):
    """Retrieve client IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def get_user_agent(request):
    """Retrieve user agent."""
    return request.META.get('HTTP_USER_AGENT', '')


def get_tokens_for_user(user):
    """Generate JWT tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def can_manage_user(request_user, target_user):
    if request_user.is_superuser or request_user.role == "superadmin":
        return True
    if (
        request_user.role == "admin"
        and target_user.branch == request_user.branch
        and target_user.role != "superadmin"
    ):
        return True
    return False


def blacklist_user_sessions(user):
    """Blacklist all active sessions for a user."""
    sessions = UserSession.objects.filter(user=user, is_active=True)
    for session in sessions:
        try:
            RefreshToken(session.refresh_token).blacklist()
        except Exception:
            pass
    sessions.update(is_active=False)


# ================= LOGIN ================= #

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        ip = get_client_ip(request)
        user_agent = get_user_agent(request)

        if serializer.is_valid():
            user = serializer.validated_data
            tokens = get_tokens_for_user(user)
            device_id = request.data.get("device_id", "unknown")

            # Deactivate previous sessions
            UserSession.objects.filter(user=user, is_active=True).update(is_active=False)

            # Create new session
            UserSession.objects.create(
                user=user,
                device_id=device_id,
                refresh_token=tokens['refresh'],
                ip_address=ip,
                user_agent=user_agent,
                is_active=True
            )

            # Log successful login
            LoginLog.objects.create(
                user=user,
                ip_address=ip,
                user_agent=user_agent,
                status='success'
            )

            update_last_login(None, user)

            return Response({
                "success": True,
                "user": UserSerializer(user).data,
                "tokens": tokens
            }, status=status.HTTP_200_OK)

        # Log failed login
        LoginLog.objects.create(
            user=None,
            ip_address=ip,
            user_agent=user_agent,
            status='failed'
        )

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# ================= TOKEN REFRESH ================= #

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        old_refresh = request.data.get("refresh")

        try:
            response = super().post(request, *args, **kwargs)
        except TokenError:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_refresh = response.data.get("refresh")

        if old_refresh and new_refresh:
            session = UserSession.objects.filter(
                refresh_token=old_refresh,
                is_active=True
            ).first()

            if session:
                session.refresh_token = new_refresh
                session.save()

        return response


# ================= PROFILE ================= #

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "success": True,
            "data": UserSerializer(request.user).data
        })


# ================= CREATE STAFF ================= #

class CreateStaffView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = CreateStaffSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            # Admin can only create staff within their branch
            if not (request.user.is_superuser or request.user.role == "superadmin"):
                serializer.save(branch=request.user.branch)
            else:
                serializer.save()

            return Response({
                "success": True,
                "message": "Staff created successfully"
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# ================= LOGOUT ================= #

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        session = UserSession.objects.filter(
            user=request.user,
            refresh_token=refresh_token,
            is_active=True
        ).first()

        if not session:
            return Response(
                {"error": "Invalid session"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            return Response(
                {"error": "Token invalid or expired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        session.is_active = False
        session.save()

        # Update logout time
        log = LoginLog.objects.filter(
            user=request.user,
            logout_time__isnull=True
        ).last()

        if log:
            log.logout_time = timezone.now()
            log.save()

        return Response({
            "success": True,
            "message": "Logged out successfully"
        })


# ================= LOGOUT ALL DEVICES ================= #
class LogoutAllDevicesView(APIView):
    """
    Logout users from all devices based on role hierarchy.

    Super Admin/Superuser: Can logout all users across branches.
    Admin: Can logout users within their own branch.
    Other Users: Can logout only themselves.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Determine accessible sessions
        if user.is_superuser or getattr(user, "role", None) == "superadmin":
            sessions = UserSession.objects.filter(is_active=True)

        elif getattr(user, "role", None) == "admin":
            sessions = UserSession.objects.filter(
                user__branch=user.branch,
                is_active=True
            )

        else:
            sessions = UserSession.objects.filter(
                user=user,
                is_active=True
            )

        # Blacklist tokens
        for session in sessions:
            try:
                RefreshToken(session.refresh_token).blacklist()
            except Exception:
                pass

        # Deactivate sessions
        count = sessions.update(is_active=False)

        return Response({
            "success": True,
            "message": f"Logged out from {count} device(s)."
        }, status=status.HTTP_200_OK)


# ================= LOGOUT ALL EXCEPT CURRENT ================= #

class LogoutAllExceptOwnView(APIView):
    """
    Logout from all devices except the current one.

    Super Admin/Superuser: Can logout all users except the current session.
    Admin: Can logout users within their own branch.
    Other Users: Can logout their own other sessions.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_refresh = request.data.get("refresh")

        if not current_refresh:
            return Response(
                {"error": "Refresh token required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user

        # Determine accessible sessions
        if user.is_superuser or getattr(user, "role", None) == "superadmin":
            sessions = UserSession.objects.filter(is_active=True)

        elif getattr(user, "role", None) == "admin":
            sessions = UserSession.objects.filter(
                user__branch=user.branch,
                is_active=True
            )

        else:
            sessions = UserSession.objects.filter(
                user=user,
                is_active=True
            )

        # Exclude current session
        sessions = sessions.exclude(refresh_token=current_refresh)

        # Blacklist tokens
        for session in sessions:
            try:
                RefreshToken(session.refresh_token).blacklist()
            except Exception:
                pass

        # Deactivate sessions
        count = sessions.update(is_active=False)

        return Response({
            "success": True,
            "message": f"Logged out from {count} other device(s)."
        }, status=status.HTTP_200_OK)
    
# ================= LOGOUT BRANCH WISE ================= #
class LogoutBranchView(APIView):
    """
    Logout all users from a particular branch.

    Permissions:
    - Super Admin/Superuser: Can logout any branch.
    - Admin: Can logout only their own branch.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        branch_id = request.data.get("branch_id")

        if not branch_id:
            return Response(
                {"error": "Branch ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate branch
        try:
            branch = Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            return Response(
                {"error": "Branch not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        user = request.user

        # Permission checks
        if user.is_superuser or getattr(user, "role", None) == "superadmin":
            pass  # Full access
        elif getattr(user, "role", None) == "admin":
            if user.branch_id != branch.id:
                return Response(
                    {"error": "You can only logout users from your own branch"},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Fetch active sessions for the branch
        sessions = UserSession.objects.filter(
            user__branch=branch,
            is_active=True
        )

        # Blacklist tokens
        logged_out_count = 0
        for session in sessions:
            try:
                RefreshToken(session.refresh_token).blacklist()
                logged_out_count += 1
            except Exception:
                pass

        # Deactivate sessions
        sessions.update(is_active=False)

        return Response({
            "success": True,
            "message": f"Logged out {logged_out_count} user(s) from {branch.name}.",
            "branch": branch.name
        }, status=status.HTTP_200_OK)
    
# ================= ADMIN RESET PASSWORD ================= #

class AdminResetPasswordView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = AdminResetPasswordSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Password reset successfully"
            })

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# ================= DEACTIVATE USER ================= #

class DeactivateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if not can_manage_user(request.user, target_user):
            return Response({"error": "Permission denied"}, status=403)

        if request.user == target_user:
            return Response(
                {"error": "You cannot deactivate yourself"},
                status=400
            )

        blacklist_user_sessions(target_user)
        target_user.is_active = False
        target_user.save()

        return Response({
            "success": True,
            "message": "User deactivated successfully"
        })


# ================= REACTIVATE USER ================= #

class ReactivateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if not can_manage_user(request.user, target_user):
            return Response({"error": "Permission denied"}, status=403)

        target_user.is_active = True
        target_user.save()

        return Response({
            "success": True,
            "message": "User reactivated successfully"
        })


# ================= DELETE USER ================= #

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        if not request.user.is_superuser:
            return Response(
                {"error": "Only superuser can delete users"},
                status=403
            )

        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if request.user == target_user:
            return Response(
                {"error": "You cannot delete yourself"},
                status=400
            )

        blacklist_user_sessions(target_user)
        target_user.delete()

        return Response({
            "success": True,
            "message": "User deleted permanently"
        })


# ================= LIST + FILTER + SEARCH USERS ================= #

class UserListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.all()

        if not (user.is_superuser or user.role == "superadmin"):
            queryset = queryset.filter(branch=user.branch)

        role = self.request.query_params.get("role")
        is_active = self.request.query_params.get("is_active")
        search = self.request.query_params.get("search")

        if role:
            queryset = queryset.filter(role=role)

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search)
            )

        return queryset.order_by("-id")


# ================= BULK USER ACTIONS ================= #

class BulkUserActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        action = request.data.get("action")
        user_ids = request.data.get("user_ids", [])

        if not user_ids:
            return Response(
                {"error": "No users selected"},
                status=status.HTTP_400_BAD_REQUEST
            )

        users = User.objects.filter(id__in=user_ids)

        if not (request.user.is_superuser or request.user.role == "superadmin"):
            users = users.filter(branch=request.user.branch)

        users = users.exclude(id=request.user.id)

        if action == "deactivate":
            for user in users:
                blacklist_user_sessions(user)
                user.is_active = False
                user.save()

        elif action == "reactivate":
            users.update(is_active=True)

        elif action == "delete":
            if not request.user.is_superuser:
                return Response(
                    {"error": "Only superuser can delete users"},
                    status=403
                )
            for user in users:
                blacklist_user_sessions(user)
                user.delete()
        else:
            return Response(
                {"error": "Invalid action"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "success": True,
            "message": f"{action.capitalize()} completed successfully"
        })

# ================= FILTER USERS STATUS (ACTIVE / INACTIVE) ================= #
class UserFilterView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user

        # ================= BASE QUERY ================= #
        if user.is_superuser or getattr(user, "role", None) == "superadmin":
            queryset = User.objects.all()
        else:
            queryset = User.objects.filter(branch=user.branch)

        # ================= FILTERS ================= #
        role = self.request.query_params.get("role")
        is_active = self.request.query_params.get("is_active")
        branch_id = self.request.query_params.get("branch_id")
        search = self.request.query_params.get("search")

        if role:
            queryset = queryset.filter(role=role)

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        if branch_id:
            if user.is_superuser or getattr(user, "role", None) == "superadmin":
                queryset = queryset.filter(branch_id=branch_id)

        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search)
            )

        return queryset.order_by("-id")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        })