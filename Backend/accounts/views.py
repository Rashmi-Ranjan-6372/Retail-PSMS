from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import AdminResetPasswordSerializer, LoginSerializer, UserSerializer, CreateStaffSerializer
from .permissions import IsAdmin
from django.contrib.auth import get_user_model
from .models import LoginLog
from django.utils.timezone import now
from rest_framework.permissions import AllowAny
User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data
            tokens = get_tokens_for_user(user)

            LoginLog.objects.create(
                user=user,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )

            return Response({
                "user": UserSerializer(user).data,
                "tokens": tokens
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


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
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        log = LoginLog.objects.filter(
            user=request.user,
            logout_time__isnull=True
        ).last()

        if log:
            log.logout_time = now()
            log.save()

        return Response({"message": "Logged out successfully"})
    
class AdminResetPasswordView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = AdminResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Password reset successfully by admin"
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)