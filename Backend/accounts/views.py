from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    AdminResetPasswordSerializer,
    LoginSerializer,
    UserSerializer,
    CreateStaffSerializer
)
from .permissions import IsAdmin
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from .models import LoginLog, UserSession

User = get_user_model()


# ================= TOKEN GENERATION ================= #
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

        if serializer.is_valid():
            user = serializer.validated_data
            tokens = get_tokens_for_user(user)

            device_id = request.data.get("device_id", "unknown")

            UserSession.objects.filter(user=user, is_active=True).update(is_active=False)

            UserSession.objects.create(
                user=user,
                device_id=device_id,
                refresh_token=tokens['refresh'],
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )

            LoginLog.objects.create(
                user=user,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT'),
                status='success'
            )

            user.last_login = now()
            user.save()

            return Response({
                "user": UserSerializer(user).data,
                "tokens": tokens
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ================= PROFILE ================= #
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            UserSerializer(request.user).data,
            status=status.HTTP_200_OK
        )


# ================= CREATE STAFF ================= #
class CreateStaffView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = CreateStaffSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Staff created successfully"
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ================= LOGOUT ================= #
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            token = RefreshToken(refresh_token)
            token.blacklist()

            UserSession.objects.filter(
                user=request.user,
                refresh_token=refresh_token,
                is_active=True
            ).update(is_active=False)

            log = LoginLog.objects.filter(
                user=request.user,
                logout_time__isnull=True
            ).last()

            if log:
                log.logout_time = now()
                log.save()

        except Exception:
            return Response({"error": "Invalid token"}, status=400)

        return Response({"message": "Logged out successfully"})


# ================= LOGOUT ALL DEVICES ================= #
class LogoutAllDevicesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Superuser → logout everyone
        if user.is_superuser:
            sessions = UserSession.objects.filter(is_active=True)

        # Admin → logout all staff
        elif user.role == 'admin':
            sessions = UserSession.objects.filter(
                user__role='staff',
                is_active=True
            )

        #  Staff → logout own devices
        else:
            sessions = UserSession.objects.filter(
                user=user,
                is_active=True
            )

        # Blacklist tokens
        for session in sessions:
            try:
                RefreshToken(session.refresh_token).blacklist()
            except:
                pass

        sessions.update(is_active=False)

        return Response({"message": "Logged out from all devices"})

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
                "message": "Password reset successfully"
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# ================= LOGOUT ALL DEVICES EXCEPT OWN ================= #
class LogoutAllExceptOwnView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_refresh = request.data.get("refresh")

        if not current_refresh:
            return Response(
                {"error": "Refresh token required"},
                status=400
            )

        user = request.user

        # ================= SUPERUSER ================= #
        if user.is_superuser:
            sessions = UserSession.objects.filter(
                is_active=True
            ).exclude(refresh_token=current_refresh)

        # ================= ADMIN ================= #
        elif user.role == 'admin':
            sessions = UserSession.objects.filter(
                user__role='staff', 
                is_active=True
            ).exclude(refresh_token=current_refresh)

        # ================= STAFF ================= #
        else:
            sessions = UserSession.objects.filter(
                user=user,
                is_active=True
            ).exclude(refresh_token=current_refresh)

        for session in sessions:
            try:
                RefreshToken(session.refresh_token).blacklist()
            except:
                pass

        sessions.update(is_active=False)

        return Response({
            "message": "Logout operation completed successfully"
        })