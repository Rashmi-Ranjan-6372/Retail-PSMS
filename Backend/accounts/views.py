from urllib3 import request

from config import settings
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
from django.db import transaction
from django.contrib.auth import authenticate
from django.core.mail import send_mail
import random
from datetime import timedelta
from .serializers import (
    AdminResetPasswordSerializer,
    LoginSerializer,
    RetailerSubscriptionListSerializer,
    UserSerializer,
    CreateStaffSerializer,
    RetailerCreateSerializer,
    VerifyOTPSerializer,
    ResendOTPSerializer,
    AssignSubscriptionSerializer,
    RetailerSerializer,
)

from .permissions import (IsAdmin, IsRetailerOwnerOrPlatformOwner)
from .models import AuditLog, LoginLog, Retailer, UserSession, EmailOTP
from subscriptions.utils import validate_branch_subscription, validate_user_subscription, check_subscription_write_access
User = get_user_model()

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


def get_user_agent(request):
    return request.META.get("HTTP_USER_AGENT", "")


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    refresh["user_id"] = user.id
    refresh["username"] = user.username
    refresh["role"] = user.role

    if user.retailer_id:
        refresh["retailer_id"] = user.retailer_id

    if user.branch_id:
        refresh["branch_id"] = user.branch_id

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def can_manage_user(request_user, target_user):

    if request_user.is_superuser:
        return True

    if (
        getattr(request_user, "role", None) == "superadmin" and
        request_user.retailer_id == target_user.retailer_id and
        target_user.role != "superadmin"
    ):
        return True

    if (
        getattr(request_user, "role", None) == "admin" and
        request_user.retailer_id == target_user.retailer_id and
        request_user.branch_id == target_user.branch_id and
        target_user.role not in ["superadmin", "admin"]
    ):
        return True

    return False


def blacklist_user_sessions(user):

    sessions = UserSession.objects.filter(
        user=user,
        is_active=True
    )

    for session in sessions:
        try:
            RefreshToken(session.refresh_token).blacklist()
        except Exception:
            pass

    sessions.update(
        is_active=False,
        revoked_at=timezone.now()
    )


def create_audit_log(
    user,
    action,
    model_name,
    object_id="",
    description="",
    request=None
):
    try:
        AuditLog.objects.create(
            user=user,
            action=action,
            model_name=model_name,
            object_id=str(object_id),
            description=description,
            ip_address=get_client_ip(request) if request else None,
            retailer=getattr(user, "retailer", None) if user else None,
            branch=getattr(user, "branch", None) if user else None,
        )
    except Exception:
        pass

# =====================================================
#                 CREATE RETAILER
# =====================================================

class CreateRetailerView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRetailerOwnerOrPlatformOwner
    ]

    def post(self, request):

        if not request.user.is_superuser:
            return Response({
                "success": False,
                "message": "Only platform owner can create retailer"
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = RetailerCreateSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():

            with transaction.atomic():
                data = serializer.save()

            create_audit_log(
                user=request.user,
                action="create",
                model_name="Retailer",
                object_id=data["retailer"].id,
                description=f"Created retailer {data['retailer'].name}",
                request=request
            )

            return Response({
                "success": True,
                "message": "Retailer created successfully",
                "retailer": {
                            "id": data["retailer"].id,
                            "name": data["retailer"].name,
                            "email": data["retailer"].email,
                        },
                "branch": {
                            "id": data["branch"].id,
                            "name": data["branch"].name,
                        },
                "superadmin": {
                                "id": data["user"].id,
                                "username": data["user"].username,
                                "role": data["user"].role,
                            }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
# =====================================================
#                 ASSIGN SUBSCRIPTION
# =====================================================
class AssignSubscriptionView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if not request.user.is_superuser:
            return Response(
                {
                    "success": False,
                    "message": "Only Platform Owner can assign subscriptions"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = AssignSubscriptionSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        subscription = serializer.save()

        create_audit_log(
            user=request.user,
            action="create",
            model_name="RetailerSubscription",
            object_id=subscription.id,
            description=(
                f"Assigned {subscription.plan.name} plan "
                f"to retailer {subscription.retailer.name}"
            ),
            request=request
        )

        return Response(
            {
                "success": True,
                "message": "Subscription assigned successfully",
                "data": {
                    "retailer": subscription.retailer.name,
                    "plan": subscription.plan.name,
                    "start_date": subscription.start_date,
                    "expiry_date": subscription.expiry_date,
                    "status": subscription.status,
                }
            },
            status=status.HTTP_201_CREATED
        )

# =====================================================
# RETAILER LIST WITH SUBSCRIPTION
# =====================================================

class RetailerSubscriptionListView(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = RetailerSubscriptionListSerializer

    def get_queryset(self):

        if not self.request.user.is_superuser:
            return Retailer.objects.none()

        return Retailer.objects.select_related(
            "subscription",
            "subscription__plan"
        ).order_by("-created_at")

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        })

# =====================================================
#                   UPDATE RETAILER
# =====================================================
class UpdateRetailerView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, retailer_id):

        if not request.user.is_superuser:
            return Response(
                {"error": "Permission denied"},
                status=403
            )

        try:
            retailer = Retailer.objects.get(
                id=retailer_id,
                is_deleted=False
            )

        except Retailer.DoesNotExist:
            return Response(
                {"error": "Retailer not found"},
                status=404
            )

        serializer = RetailerCreateSerializer(
            retailer,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            create_audit_log(
                user=request.user,
                action="update",
                model_name="Retailer",
                object_id=retailer.id,
                description=f"Updated retailer {retailer.name}",
                request=request
            )

            return Response({
                "success": True,
                "message": "Retailer updated successfully",
                "data": serializer.data
            })

        return Response(
            serializer.errors,
            status=400
        )

# =====================================================
#                  HARD DELETE RETAILER
# =====================================================
class HardDeleteRetailerView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, retailer_id):

        if not request.user.is_superuser:
            return Response(
                {"error": "Permission denied"},
                status=403
            )

        try:
            retailer = Retailer.objects.get(
                id=retailer_id
            )

        except Retailer.DoesNotExist:
            return Response(
                {"error": "Retailer not found"},
                status=404
            )

        retailer_name = retailer.name

        retailer.delete()

        create_audit_log(
            user=request.user,
            action="delete",
            model_name="Retailer",
            object_id=retailer_id,
            description=f"Hard deleted retailer {retailer_name}",
            request=request
        )

        return Response({
            "success": True,
            "message": "Retailer permanently deleted"
        })

# =====================================================
#                  REACTIVATE RETAILER
# =====================================================
class ReactivateRetailerView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, retailer_id):

        if not request.user.is_superuser:
            return Response(
                {"error": "Permission denied"},
                status=403
            )

        try:
            retailer = Retailer.objects.get(
                id=retailer_id,
                is_deleted=False
            )

        except Retailer.DoesNotExist:
            return Response(
                {"error": "Retailer not found"},
                status=404
            )

        retailer.is_active = True
        retailer.save()

        create_audit_log(
            user=request.user,
            action="update",
            model_name="Retailer",
            object_id=retailer.id,
            description=f"Reactivated retailer {retailer.name}",
            request=request
        )

        return Response({
            "success": True,
            "message": "Retailer reactivated successfully"
        })
    

# =====================================================
#                  DEACTIVATE RETAILER
# ====================================================
class DeactivateRetailerView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, retailer_id):

        if not request.user.is_superuser:
            return Response(
                {"error": "Permission denied"},
                status=403
            )

        try:
            retailer = Retailer.objects.get(
                id=retailer_id,
                is_deleted=False
            )

        except Retailer.DoesNotExist:
            return Response(
                {"error": "Retailer not found"},
                status=404
            )

        retailer.is_active = False
        retailer.save()

        User.objects.filter(
            retailer=retailer
        ).update(is_active=False)

        create_audit_log(
            user=request.user,
            action="update",
            model_name="Retailer",
            object_id=retailer.id,
            description=f"Deactivated retailer {retailer.name}",
            request=request
        )

        return Response({
            "success": True,
            "message": "Retailer deactivated successfully"
        })
    
# =================================================
#                RETAILER FILTER
# =================================================
class RetailerFilterView(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = RetailerSerializer

    def get_queryset(self):

        if not self.request.user.is_superuser:
            return Retailer.objects.none()

        queryset = Retailer.objects.select_related(
            "subscription",
            "subscription__plan"
        )

        search = self.request.query_params.get("search")
        is_active = self.request.query_params.get("is_active")
        plan_id = self.request.query_params.get("plan_id")
        subscription_status = self.request.query_params.get("subscription_status")

        # ================= SEARCH =================

        if search:

            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(owner_name__icontains=search) |
                Q(email__icontains=search) |
                Q(mobile__icontains=search)
            )

        # ================= ACTIVE FILTER =================

        if is_active is not None:

            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        # ================= PLAN FILTER =================

        if plan_id:

            queryset = queryset.filter(
                subscription__plan_id=plan_id
            )

        # ================= STATUS FILTER =================

        if subscription_status:

            queryset = queryset.filter(
                subscription__status=subscription_status
            )

        return queryset.order_by("-created_at")

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        })

# =====================================================
# LOGIN
# =====================================================
class LoginView(APIView):
    permission_classes = [AllowAny]
    MAX_ACTIVE_DEVICES = 3

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        ip = get_client_ip(request)
        user_agent = get_user_agent(request)

        if not serializer.is_valid():

            LoginLog.objects.create(
                ip_address=ip,
                user_agent=user_agent,
                status="failed"
            )

            create_audit_log(
                user=None,
                action="login",
                model_name="UserSession",
                object_id="failed",
                description="Failed login attempt",
                request=request
            )

            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data

        # =====================================================
        #               ACCOUNT LOCKOUT CHECK
        # =====================================================

        if user.is_account_locked():

            return Response({
                "success": False,
                "message":
                f"Account locked until {user.account_locked_until}"
            }, status=status.HTTP_403_FORBIDDEN)

        if not user.is_active:

            return Response({
                "success": False,
                "message": "Account is inactive"
            }, status=status.HTTP_403_FORBIDDEN)

        user.failed_login_attempts = 0
        user.account_locked_until = None
        user.save(
            update_fields=[
                "failed_login_attempts",
                "account_locked_until"
            ]
        )

        # =====================================================
        # EMAIL OTP FOR SUPERADMIN & ADMIN
        # =====================================================

        if user.role in ["superadmin", "admin"]:

            otp = str(
                random.randint(
                    100000,
                    999999
                )
            )

            EmailOTP.objects.filter(
                user=user
            ).delete()

            EmailOTP.objects.create(
                user=user,
                otp=otp,
                expires_at=timezone.now() +
                timedelta(minutes=5)
            )

            send_mail(
                subject="Retail PSMS Login OTP",
                message=f"Your OTP is {otp}. Valid for 5 minutes.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False
            )

            create_audit_log(
                user=user,
                action="login",
                model_name="EmailOTP",
                object_id=user.id,
                description="OTP sent for login verification",
                request=request
            )

            return Response({
                "success": True,
                "otp_required": True,
                "user_id": user.id,
                "message":
                "OTP has been sent to your registered email."
            }, status=status.HTTP_200_OK)

        # =====================================================
        # NORMAL LOGIN FOR OTHER ROLES
        # =====================================================

        device_id = request.data.get(
            "device_id",
            "unknown"
        )

        active_sessions = UserSession.objects.filter(
            user=user,
            is_active=True
        ).order_by("created_at")

        if active_sessions.count() >= self.MAX_ACTIVE_DEVICES:

            oldest_session = active_sessions.first()

            try:
                RefreshToken(
                    oldest_session.refresh_token
                ).blacklist()
            except Exception:
                pass

            oldest_session.is_active = False
            oldest_session.revoked_at = timezone.now()

            oldest_session.save(
                update_fields=[
                    "is_active",
                    "revoked_at"
                ]
            )

        tokens = get_tokens_for_user(user)

        session = UserSession.objects.create(
            user=user,
            retailer_id=user.retailer_id,
            branch_id=user.branch_id,
            device_id=device_id,
            refresh_token=tokens["refresh"],
            ip_address=ip,
            user_agent=user_agent,
            is_active=True
        )

        LoginLog.objects.create(
            user=user,
            retailer=user.retailer,
            branch=user.branch,
            ip_address=ip,
            user_agent=user_agent,
            status="success"
        )

        create_audit_log(
            user=user,
            action="login",
            model_name="UserSession",
            object_id=session.id,
            description=f"User logged in from device {device_id}",
            request=request
        )

        update_last_login(None, user)

        return Response({
            "success": True,
            "user": UserSerializer(user).data,
            "tokens": tokens
        }, status=status.HTTP_200_OK)

# =====================================================
#                  VERIFY OTP
# =====================================================
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    MAX_ACTIVE_DEVICES = 3

    def post(self, request):

        serializer = VerifyOTPSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data["user"]
        otp = serializer.validated_data["otp"]

        try:

            otp_obj = EmailOTP.objects.get(
                user=user,
                otp=otp,
                is_verified=False
            )

        except EmailOTP.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Invalid OTP"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if otp_obj.expires_at < timezone.now():

            otp_obj.delete()

            return Response(
                {
                    "success": False,
                    "message": "OTP expired"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        otp_obj.delete()

        ip = get_client_ip(request)
        user_agent = get_user_agent(request)

        device_id = request.data.get(
            "device_id",
            "unknown"
        )

        active_sessions = UserSession.objects.filter(
            user=user,
            is_active=True
        ).order_by("created_at")

        if active_sessions.count() >= self.MAX_ACTIVE_DEVICES:

            oldest_session = active_sessions.first()

            try:
                RefreshToken(
                    oldest_session.refresh_token
                ).blacklist()
            except Exception:
                pass

            oldest_session.is_active = False
            oldest_session.revoked_at = timezone.now()

            oldest_session.save(
                update_fields=[
                    "is_active",
                    "revoked_at"
                ]
            )

        refresh = RefreshToken.for_user(user)

        session = UserSession.objects.create(
            user=user,
            retailer=user.retailer,
            branch=user.branch,
            device_id=device_id,
            refresh_token=str(refresh),
            ip_address=ip,
            user_agent=user_agent,
            is_active=True
        )

        LoginLog.objects.create(
            user=user,
            retailer=user.retailer,
            branch=user.branch,
            ip_address=ip,
            user_agent=user_agent,
            status="success"
        )

        create_audit_log(
            user=user,
            action="login",
            model_name="UserSession",
            object_id=session.id,
            description=f"OTP verified and login completed from {device_id}",
            request=request
        )

        return Response(
            {
                "success": True,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )

# =====================================================
#                  RESEND OTP
# =====================================================
class ResendOTPView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ResendOTPSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data["user"]

        EmailOTP.objects.filter(
            user=user
        ).delete()

        otp = str(
            random.randint(
                100000,
                999999
            )
        )

        EmailOTP.objects.create(
            user=user,
            otp=otp,
            expires_at=timezone.now() +
            timedelta(minutes=5)
        )

        send_mail(
            subject="Retail PSMS Login OTP",
            message=(
                f"Dear {user.username},\n\n"
                f"Your login OTP is: {otp}\n\n"
                f"This OTP is valid for 5 minutes."
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[
                user.email
            ],
            fail_silently=False
        )

        create_audit_log(
            user=user,
            action="login",
            model_name="EmailOTP",
            object_id=user.id,
            description="OTP resent successfully",
            request=request
        )

        return Response(
            {
                "success": True,
                "message":
                "OTP resent successfully"
            },
            status=status.HTTP_200_OK
        )
    
# =====================================================
# TOKEN REFRESH
# =====================================================
class CustomTokenRefreshView(TokenRefreshView):

    serializer_class = TokenRefreshSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        old_refresh = request.data.get("refresh")

        try:
            response = super().post(request, *args, **kwargs)

        except TokenError:
            return Response({
                "success": False,
                "error": "Invalid or expired token"
            }, status=status.HTTP_400_BAD_REQUEST)

        new_refresh = response.data.get("refresh")

        if old_refresh and new_refresh:

            session = UserSession.objects.filter(
                refresh_token=old_refresh,
                is_active=True
            ).first()

            if session:
                session.refresh_token = new_refresh
                session.save(update_fields=["refresh_token"])

        return response

# =====================================================
#                        PROFILE 
# =====================================================

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({
            "success": True,
            "data": UserSerializer(request.user).data
        })


# =====================================================
# CREATE STAFF
# =====================================================
class CreateStaffView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):

        serializer = CreateStaffSerializer(
            data=request.data,
            context={"request": request}
        )

        if not serializer.is_valid():

            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # ==========================================
        # PLATFORM OWNER
        # ==========================================
        if request.user.is_superuser:

            retailer_id = request.data.get("retailer")
            branch_id = request.data.get("branch")

            if not retailer_id or not branch_id:
                return Response({
                    "success": False,
                    "message": "Retailer and branch are required"
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                retailer = Retailer.objects.get(
                    id=retailer_id
                )

            except Retailer.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "Retailer not found"
                }, status=status.HTTP_404_NOT_FOUND)

            # Subscription validations
            check_subscription_write_access(retailer)
            validate_user_subscription(retailer)

            branch = Branch.objects.filter(
                id=branch_id,
                retailer_id=retailer_id
            ).first()

            if not branch:
                return Response({
                    "success": False,
                    "message": "Branch does not belong to retailer"
                }, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save(
                retailer=retailer,
                branch=branch
            )

        # ==========================================
        # RETAILER OWNER (SUPERADMIN)
        # ==========================================
        elif request.user.role == "superadmin":

            check_subscription_write_access(
                request.user.retailer
            )

            validate_user_subscription(
                request.user.retailer
            )

            branch_id = request.data.get("branch")

            if not branch_id:
                return Response({
                    "success": False,
                    "message": "Branch is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            branch = Branch.objects.filter(
                id=branch_id,
                retailer=request.user.retailer
            ).first()

            if not branch:
                return Response({
                    "success": False,
                    "message": "Invalid branch"
                }, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save(
                retailer=request.user.retailer,
                branch=branch
            )

        # ==========================================
        # ADMIN
        # ==========================================
        else:

            check_subscription_write_access(
                request.user.retailer
            )

            validate_user_subscription(
                request.user.retailer
            )

            user = serializer.save(
                retailer=request.user.retailer,
                branch=request.user.branch
            )

        create_audit_log(
            user=request.user,
            action="create",
            model_name="User",
            object_id=user.id,
            description=f"Created user {user.username}",
            request=request
        )

        return Response({
            "success": True,
            "message": "Staff created successfully",
            "data": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


# ================= LOGOUT ================= #

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({
                "error": "Refresh token required"
            }, status=status.HTTP_400_BAD_REQUEST)

        session = UserSession.objects.filter(
            user=request.user,
            refresh_token=refresh_token,
            is_active=True
        ).first()

        if not session:
            return Response({
                "error": "Invalid session"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            RefreshToken(refresh_token).blacklist()

        except TokenError:
            return Response({
                "error": "Token invalid or expired"
            }, status=status.HTTP_400_BAD_REQUEST)

        session.is_active = False
        session.revoked_at = timezone.now()
        session.save(update_fields=["is_active", "revoked_at"])

        log = LoginLog.objects.filter(
            user=request.user,
            logout_time__isnull=True
        ).last()

        if log:
            log.logout_time = timezone.now()
            log.save(update_fields=["logout_time"])

        create_audit_log(
            user=request.user,
            action="logout",
            model_name="UserSession",
            object_id=session.id,
            description="User logged out from device",
            request=request
        )

        return Response({
            "success": True,
            "message": "Logged out successfully"
        })
    

# ================= LOGOUT ALL DEVICES ================= #

class LogoutAllDevicesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        # ================= PLATFORM OWNER =================
        if user.is_superuser:

            retailer_id = request.data.get("retailer_id")

            if not retailer_id:
                return Response({
                    "error": "retailer_id required for platform logout"
                }, status=status.HTTP_400_BAD_REQUEST)

            sessions = UserSession.objects.filter(
                user__retailer_id=retailer_id,
                is_active=True
            )

        # ================= RETAILER SUPERADMIN =================
        elif user.role == "superadmin":

            sessions = UserSession.objects.filter(
                user__retailer_id=user.retailer_id,
                is_active=True
            )

        # ================= ADMIN =================
        elif user.role == "admin":

            sessions = UserSession.objects.filter(
                user__retailer_id=user.retailer_id,
                user__branch_id=user.branch_id,
                is_active=True
            )

        # ================= NORMAL USER =================
        else:

            sessions = UserSession.objects.filter(
                user=user,
                is_active=True
            )

        count = sessions.count()

        for session in sessions:
            try:
                RefreshToken(session.refresh_token).blacklist()
            except Exception:
                pass

        sessions.update(is_active=False)

        create_audit_log(
            user=request.user,
            action="logout",
            model_name="UserSession",
            object_id="all_devices",
            description=f"Logged out {count} devices",
            request=request
        )
                
        return Response({
            "success": True,
            "message": f"Logged out from {count} device(s)."
        }, status=status.HTTP_200_OK)


# ================= LOGOUT ALL EXCEPT CURRENT ================= #

class LogoutAllExceptOwnView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        current_refresh = request.data.get("refresh")
        retailer_id = request.data.get("retailer_id")

        if not current_refresh:
            return Response({"error": "Refresh token required"}, status=400)

        user = request.user

        if user.is_superuser:

            if not retailer_id:
                return Response({
                    "error": "retailer_id required for superuser"
                }, status=400)

            sessions = UserSession.objects.filter(
                user__retailer_id=retailer_id,
                is_active=True
            )

        elif user.role == "superadmin":
            sessions = UserSession.objects.filter(
                user__retailer_id=user.retailer_id,
                is_active=True
            )

        elif user.role == "admin":
            sessions = UserSession.objects.filter(
                user__retailer_id=user.retailer_id,
                user__branch_id=user.branch_id,
                is_active=True
            )

        else:
            sessions = UserSession.objects.filter(
                user=user,
                is_active=True
            )

        sessions = sessions.exclude(refresh_token=current_refresh)

        count = sessions.count()

        for session in sessions:
            try:
                RefreshToken(session.refresh_token).blacklist()
            except Exception:
                pass

        sessions.update(is_active=False)

        create_audit_log(
            user=request.user,
            action="logout",
            model_name="UserSession",
            object_id="except_current",
            description=f"Logged out {count} other sessions",
            request=request
        )

        return Response({
            "success": True,
            "message": f"Logged out from {count} other device(s)."
        }, status=200)


# ================= LOGOUT BRANCH ================= #

class LogoutBranchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        branch_id = request.data.get("branch_id")

        if not branch_id:
            return Response({
                "error": "Branch ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            branch = Branch.objects.get(id=branch_id)

        except Branch.DoesNotExist:
            return Response({
                "error": "Branch not found"
            }, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # Django Superuser
        if user.is_superuser:
            pass

        # Retailer SuperAdmin
        elif user.role == "superadmin":

            if user.retailer != branch.retailer:
                return Response({
                    "error": "You can only logout users from your own retailer"
                }, status=status.HTTP_403_FORBIDDEN)

        # Admin
        elif user.role == "admin":

            if (
                user.branch_id != branch.id or
                user.retailer != branch.retailer
            ):
                return Response({
                    "error": "You can only logout users from your own retailer and branch"
                }, status=status.HTTP_403_FORBIDDEN)

        else:
            return Response({
                "error": "Permission denied"
            }, status=status.HTTP_403_FORBIDDEN)

        sessions = UserSession.objects.filter(
            user__retailer=branch.retailer,
            user__branch=branch,
            is_active=True
        )

        logged_out_count = 0

        for session in sessions:
            try:
                RefreshToken(session.refresh_token).blacklist()
                logged_out_count += 1
            except Exception:

                pass

        sessions.update(is_active=False)

        create_audit_log(
            user=request.user,
            action="logout",
            model_name="UserSession",
            object_id=f"branch_{branch.id}",
            description=f"Logged out branch {branch.name}",
            request=request
        )

        return Response({
            "success": True,
            "message": f"Logged out {logged_out_count} user(s) from {branch.name}.",
            "branch": branch.name
        }, status=status.HTTP_200_OK)

# ================= ADMIN RESET PASSWORD ================= #
# ================= ADMIN RESET PASSWORD ================= #

class AdminResetPasswordView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):

        if not request.user.is_superuser:
            check_subscription_write_access(
                request.user.retailer
            )

        serializer = AdminResetPasswordSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():

            serializer.save()

            create_audit_log(
                user=request.user,
                action="update",
                model_name="User",
                object_id="password_reset",
                description="Admin reset user password",
                request=request
            )

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

        if not request.user.is_superuser:
            check_subscription_write_access(
                request.user.retailer
            )

        try:
            target_user = User.objects.get(id=user_id)

        except User.DoesNotExist:
            return Response({
                "error": "User not found"
            }, status=404)

        if not can_manage_user(
            request.user,
            target_user
        ):
            return Response({
                "error": "Permission denied"
            }, status=403)

        if request.user == target_user:
            return Response({
                "error": "You cannot deactivate yourself"
            }, status=400)

        blacklist_user_sessions(target_user)

        target_user.is_active = False
        target_user.save(update_fields=["is_active"])

        create_audit_log(
            user=request.user,
            action="update",
            model_name="User",
            object_id=target_user.id,
            description=f"Deactivated user {target_user.username}",
            request=request
        )

        return Response({
            "success": True,
            "message": "User deactivated successfully"
        })


# ================= REACTIVATE USER ================= #

class ReactivateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id):

        if not request.user.is_superuser:
            check_subscription_write_access(
                request.user.retailer
            )

        try:
            target_user = User.objects.get(id=user_id)

        except User.DoesNotExist:
            return Response({
                "error": "User not found"
            }, status=404)

        if not can_manage_user(
            request.user,
            target_user
        ):
            return Response({
                "error": "Permission denied"
            }, status=403)

        target_user.is_active = True
        target_user.save(update_fields=["is_active"])

        create_audit_log(
            user=request.user,
            action="update",
            model_name="User",
            object_id=target_user.id,
            description=f"Reactivated user {target_user.username}",
            request=request
        )

        return Response({
            "success": True,
            "message": "User reactivated successfully"
        })


# ================= DELETE USER ================= #

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):

        if not (
            request.user.is_superuser or
            request.user.role == "superadmin"
        ):
            return Response({
                "error": "Only superadmin can delete users"
            }, status=403)

        if not request.user.is_superuser:
            check_subscription_write_access(
                request.user.retailer
            )

        try:
            target_user = User.objects.get(id=user_id)

        except User.DoesNotExist:
            return Response({
                "error": "User not found"
            }, status=404)

        if request.user == target_user:
            return Response({
                "error": "You cannot delete yourself"
            }, status=400)

        blacklist_user_sessions(target_user)

        username = target_user.username

        target_user.is_deleted = True
        target_user.is_active = False

        target_user.save(
            update_fields=[
                "is_deleted",
                "is_active"
            ]
        )

        create_audit_log(
            user=request.user,
            action="delete",
            model_name="User",
            object_id=user_id,
            description=f"Deleted user {username}",
            request=request
        )

        return Response({
            "success": True,
            "message": "User deleted permanently"
        })


# ================= BULK USER ACTION ================= #
# ================= BULK USER ACTION ================= #
class BulkUserActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        if not request.user.is_superuser:
            check_subscription_write_access(
                request.user.retailer
            )

        action = request.data.get("action")
        user_ids = request.data.get("user_ids", [])

        if not user_ids:
            return Response(
                {"error": "No users selected"},
                status=400
            )

        users = User.objects.filter(
            id__in=user_ids
        ).exclude(
            id=request.user.id
        )

        if request.user.is_superuser:
            pass

        elif request.user.role == "superadmin":
            users = users.filter(
                retailer=request.user.retailer
            )

        else:
            users = users.filter(
                retailer=request.user.retailer,
                branch=request.user.branch
            )

        if not users.exists():
            return Response(
                {"error": "No valid users found"},
                status=400
            )

        affected_ids = []

        with transaction.atomic():

            if action == "deactivate":

                for user in users:
                    blacklist_user_sessions(user)

                    user.is_active = False
                    user.save(
                        update_fields=["is_active"]
                    )

                    affected_ids.append(user.id)

                audit_action = "update"
                audit_desc = (
                    f"Bulk deactivated users: {affected_ids}"
                )

            elif action == "reactivate":

                updated = users.update(
                    is_active=True
                )

                affected_ids = list(
                    users.values_list(
                        "id",
                        flat=True
                    )
                )

                audit_action = "update"
                audit_desc = (
                    f"Bulk reactivated {updated} users: "
                    f"{affected_ids}"
                )

            elif action == "delete":

                if not (
                    request.user.is_superuser or
                    request.user.role == "superadmin"
                ):
                    return Response(
                        {
                            "error":
                            "Only superadmin can delete users"
                        },
                        status=403
                    )

                for user in users:

                    affected_ids.append({
                        "id": user.id,
                        "username": user.username
                    })

                    blacklist_user_sessions(user)

                    user.is_deleted = True
                    user.is_active = False
                    user.save(
                        update_fields=[
                            "is_deleted",
                            "is_active"
                        ]
                    )

                audit_action = "delete"
                audit_desc = (
                    f"Bulk deleted users: {affected_ids}"
                )

            else:
                return Response(
                    {"error": "Invalid action"},
                    status=400
                )

            create_audit_log(
                user=request.user,
                action=audit_action,
                model_name="User",
                object_id="bulk",
                description=audit_desc,
                request=request
            )

        return Response({
            "success": True,
            "message": (
                f"{action.capitalize()} "
                "completed successfully"
            ),
            "affected_count": len(affected_ids)
        })


# ================= USER FILTER ================= #
class UserFilterView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = User.objects.select_related(
                    "retailer",
                    "branch"
                )

        elif user.role == "superadmin":
            queryset = User.objects.filter(retailer=user.retailer)

        else:
            queryset = User.objects.filter(
                retailer=user.retailer,
                branch=user.branch
            )

        role = self.request.query_params.get("role")
        is_active = self.request.query_params.get("is_active")
        retailer_id = self.request.query_params.get("retailer_id")
        branch_id = self.request.query_params.get("branch_id")
        search = self.request.query_params.get("search")

        if role:
            queryset = queryset.filter(role=role)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        if retailer_id and user.is_superuser:
            queryset = queryset.filter(retailer_id=retailer_id)

        if branch_id:
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