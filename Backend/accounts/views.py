from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.generics import ListAPIView
from django.db.models import Q

from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
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


# ================= HELPER ================= #
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# ================= LOGIN ================= #
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT')

        if serializer.is_valid():
            user = serializer.validated_data
            tokens = get_tokens_for_user(user)

            device_id = request.data.get("device_id", "unknown")

            UserSession.objects.filter(user=user, is_active=True).update(is_active=False)

            UserSession.objects.create(
                user=user,
                device_id=device_id,
                refresh_token=tokens['refresh'],
                ip_address=ip,
                user_agent=user_agent,
                is_active=True
            )

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


# ================= TOKEN REFRESH (ROTATION) ================= #
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        old_refresh = request.data.get("refresh")

        try:
            response = super().post(request, *args, **kwargs)
        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=400)

        new_refresh = response.data.get("refresh")

        if old_refresh and new_refresh:
            session = UserSession.objects.filter(
                refresh_token=old_refresh,
                is_active=True
            ).first()

            if session:
                session.refresh_token = new_refresh
                session.save()
            else:
                UserSession.objects.filter(is_active=True).update(is_active=False)

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
        serializer = CreateStaffSerializer(data=request.data)

        if serializer.is_valid():
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
            return Response({"error": "Refresh token required"}, status=400)

        session = UserSession.objects.filter(
            user=request.user,
            refresh_token=refresh_token,
            is_active=True
        ).first()

        if not session:
            return Response({"error": "Invalid session"}, status=400)

        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            return Response({"error": "Token invalid or expired"}, status=400)

        session.is_active = False
        session.save()

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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.is_superuser:
            sessions = UserSession.objects.filter(is_active=True)

        elif user.role == 'admin':
            sessions = UserSession.objects.filter(
                user__role='staff',
                is_active=True
            )

        else:
            sessions = UserSession.objects.filter(
                user=user,
                is_active=True
            )

        for session in sessions:
            try:
                RefreshToken(session.refresh_token).blacklist()
            except Exception as e:
                print("Blacklist error:", str(e))

        sessions.update(is_active=False)

        return Response({
            "success": True,
            "message": "Logged out from all devices"
        })


# ================= LOGOUT ALL EXCEPT OWN ================= #
class LogoutAllExceptOwnView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_refresh = request.data.get("refresh")

        if not current_refresh:
            return Response({"error": "Refresh token required"}, status=400)

        user = request.user

        if user.is_superuser:
            sessions = UserSession.objects.filter(
                is_active=True
            ).exclude(refresh_token=current_refresh)

        elif user.role == 'admin':
            sessions = UserSession.objects.filter(
                user__role='staff',
                is_active=True
            ).exclude(refresh_token=current_refresh)

        else:
            sessions = UserSession.objects.filter(
                user=user,
                is_active=True
            ).exclude(refresh_token=current_refresh)

        for session in sessions:
            try:
                RefreshToken(session.refresh_token).blacklist()
            except Exception as e:
                print("Blacklist error:", str(e))

        sessions.update(is_active=False)

        return Response({
            "success": True,
            "message": "Logged out from other devices"
        })


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
    
# ================= HEALPER FUNCTION ================= #
def get_target_users(request_user, target_user):
    if request_user.is_superuser:
        return True

    if request_user.role == 'admin' and target_user.role == 'staff':
        return True

    return False

# ================= DEACTIVATE USER ================= #
class DeactivateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if not get_target_users(request.user, target_user):
            return Response({"error": "Permission denied"}, status=403)

        if request.user == target_user:
            return Response({"error": "You cannot deactivate yourself"}, status=400)

        sessions = UserSession.objects.filter(user=target_user, is_active=True)

        for session in sessions:
            try:
                RefreshToken(session.refresh_token).blacklist()
            except:
                pass

        sessions.update(is_active=False)

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

        if not get_target_users(request.user, target_user):
            return Response({"error": "Permission denied"}, status=403)

        target_user.is_active = True
        target_user.save()

        return Response({
            "success": True,
            "message": "User reactivated successfully"
        })

# ================= HEARD DELETE WHICH IS ONLY DONE BY THE SUPERUSER ================= #
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        if not request.user.is_superuser:
            return Response({"error": "Only superuser can delete users"}, status=403)

        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if request.user == target_user:
            return Response({"error": "You cannot delete yourself"}, status=400)

        sessions = UserSession.objects.filter(user=target_user, is_active=True)

        for session in sessions:
            try:
                RefreshToken(session.refresh_token).blacklist()
            except:
                pass

        sessions.delete()

        target_user.delete()

        return Response({
            "success": True,
            "message": "User deleted permanently"
        })

# ================= LIST + FILTER + SEARCH USERS ================= #
class UserListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.all()

        if user.role == 'admin':
            queryset = queryset.filter(role='staff')

        role = self.request.query_params.get('role')
        is_active = self.request.query_params.get('is_active')
        search = self.request.query_params.get('search')

        if role:
            queryset = queryset.filter(role=role)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search)
            )

        return queryset.order_by('-id')
    
# ================= BULK ACTION FOR USERS ================= #
class BulkUserActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        action = request.data.get("action")
        user_ids = request.data.get("user_ids", [])

        if not user_ids:
            return Response({"error": "No users selected"}, status=400)

        users = User.objects.filter(id__in=user_ids)

        if not request.user.is_superuser:
            users = users.filter(role='staff')

        users = users.exclude(id=request.user.id)

        if action == "deactivate":
            self._deactivate(users)

        elif action == "reactivate":
            self._reactivate(users)

        elif action == "delete":
            if not request.user.is_superuser:
                return Response({"error": "Only superuser can delete"}, status=403)
            self._delete(users)

        else:
            return Response({"error": "Invalid action"}, status=400)

        return Response({
            "success": True,
            "message": f"{action} completed successfully"
        })

    def _deactivate(self, users):
        for user in users:
            sessions = UserSession.objects.filter(user=user, is_active=True)
            for session in sessions:
                try:
                    RefreshToken(session.refresh_token).blacklist()
                except:
                    pass
            sessions.update(is_active=False)
            user.is_active = False
            user.save()

    def _reactivate(self, users):
        users.update(is_active=True)

    def _delete(self, users):
        for user in users:
            sessions = UserSession.objects.filter(user=user, is_active=True)
            for session in sessions:
                try:
                    RefreshToken(session.refresh_token).blacklist()
                except:
                    pass
            sessions.delete()
            user.delete()