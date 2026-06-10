from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.utils.timezone import now
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from django.contrib.auth import get_user_model
from branches.models import Branch
from .models import Retailer, User, EmailOTP
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from subscriptions.models import SubscriptionPlan, RetailerSubscription

User = get_user_model()
class RetailerCreateSerializer(serializers.Serializer):
    retailer_name = serializers.CharField(max_length=255)
    owner_name = serializers.CharField(max_length=255)
    mobile = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    address = serializers.CharField(required=False, allow_blank=True)
    gst_number = serializers.CharField(required=False, allow_blank=True)
    license_number = serializers.CharField(required=False, allow_blank=True)
    branch_name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)

    # ======================================
    # EMAIL VALIDATION
    # ======================================

    def validate_email(self, value):

        if Retailer.objects.filter(
            email=value
        ).exists():

            raise serializers.ValidationError(
                "Retailer email already exists."
            )

        if User.objects.filter(
            email=value
        ).exists():

            raise serializers.ValidationError(
                "User email already exists."
            )

        return value

    # ======================================
    # MOBILE VALIDATION
    # ======================================

    def validate_mobile(self, value):

        if Retailer.objects.filter(
            mobile=value
        ).exists():

            raise serializers.ValidationError(
                "Mobile number already exists."
            )

        return value

    # ======================================
    # USERNAME VALIDATION
    # ======================================

    def validate_username(self, value):

        if User.objects.filter(
            username=value
        ).exists():

            raise serializers.ValidationError(
                "Username already exists."
            )

        return value

    # ======================================
    # CREATE RETAILER
    # ======================================

    @transaction.atomic
    def create(self, validated_data):

        request = self.context.get("request")

        # ==========================
        # CREATE RETAILER
        # ==========================

        retailer = Retailer.objects.create(
            name=validated_data["retailer_name"],
            owner_name=validated_data["owner_name"],
            mobile=validated_data["mobile"],
            email=validated_data["email"],
            address=validated_data.get("address", ""),
            gst_number=validated_data.get("gst_number", ""),
            license_number=validated_data.get("license_number", ""),
            created_by=request.user
        )

        # ==========================
        # DEFAULT BRANCH
        # ==========================

        branch = Branch.objects.create(
            retailer=retailer,
            name=validated_data["branch_name"],
            created_by=request.user
        )

        # ==========================
        # SUPERADMIN USER
        # ==========================

        superadmin = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role="superadmin",
            retailer=retailer,
            branch=branch,
            created_by=request.user,
            is_active=True,
            is_staff=True
        )

        return {
            "retailer": retailer,
            "branch": branch,
            "user": superadmin
        }

# =========================================================
#               SUBSCRIPTION SERIALIZERS
# =========================================================
class AssignSubscriptionSerializer(serializers.Serializer):

    retailer_id = serializers.IntegerField()
    plan_id = serializers.IntegerField()
    duration_days = serializers.IntegerField(default=30)

    def validate(self, attrs):

        try:
            attrs["retailer"] = Retailer.objects.get(
                id=attrs["retailer_id"]
            )
        except Retailer.DoesNotExist:
            raise serializers.ValidationError(
                {"retailer_id": "Retailer not found"}
            )

        try:
            attrs["plan"] = SubscriptionPlan.objects.get(
                id=attrs["plan_id"],
                is_active=True
            )
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError(
                {"plan_id": "Subscription plan not found"}
            )

        return attrs

    def save(self):

        retailer = self.validated_data["retailer"]
        plan = self.validated_data["plan"]
        duration_days = self.validated_data["duration_days"]

        start_date = timezone.now().date()
        expiry_date = start_date + timedelta(days=duration_days)

        subscription, created = RetailerSubscription.objects.update_or_create(
            retailer=retailer,
            defaults={
                "plan": plan,
                "start_date": start_date,
                "expiry_date": expiry_date,
                "status": "active"
            }
        )

        return subscription

# =======================================================================
#       SUBSCRIPTION PLAN & RETAILER SUBSCRIPTION SERIALIZERS
# =======================================================================
class RetailerSubscriptionListSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source="subscription.plan.name", read_only=True)
    plan_type = serializers.CharField(source="subscription.plan.plan_type", read_only=True)
    max_users = serializers.IntegerField(source="subscription.plan.max_users", read_only=True)
    max_branches = serializers.IntegerField(source="subscription.plan.max_branches", read_only=True)
    subscription_status = serializers.CharField(source="subscription.status", read_only=True)
    start_date = serializers.DateField(source="subscription.start_date", read_only=True)
    expiry_date = serializers.DateField(source="subscription.expiry_date", read_only=True)
    current_users = serializers.SerializerMethodField()
    current_branches = serializers.SerializerMethodField()

    class Meta:
        model = Retailer

        fields = [
            "id",
            "name",
            "owner_name",
            "mobile",
            "email",
            "is_active",

            "plan_name",
            "plan_type",
            "subscription_status",
            "start_date",
            "expiry_date",

            "max_users",
            "max_branches",

            "current_users",
            "current_branches",
        ]

    def get_current_users(self, obj):
        return User.objects.filter(
            retailer=obj,
            is_deleted=False
        ).count()

    def get_current_branches(self, obj):
        return Branch.objects.filter(
            retailer=obj,
            deleted_at__isnull=True
        ).count()

# =================================================================
#             RETAILER SERIALIZER FOR SEARCH * FILTER
# =================================================================
class RetailerSerializer(serializers.ModelSerializer):

    subscription_plan = serializers.SerializerMethodField()
    subscription_status = serializers.SerializerMethodField()

    class Meta:
        model = Retailer
        fields = [
            "id",
            "name",
            "owner_name",
            "mobile",
            "email",
            "is_active",
            "subscription_plan",
            "subscription_status",
            "created_at"
        ]

    def get_subscription_plan(self, obj):

        subscription = getattr(
            obj,
            "subscription",
            None
        )

        if subscription:
            return subscription.plan.name

        return None

    def get_subscription_status(self, obj):

        subscription = getattr(
            obj,
            "subscription",
            None
        )

        if subscription:
            return subscription.status

        return "No Subscription"

# ================= USER SERIALIZER ================= #

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'email',
            'role',
            'phone',
            'retailer',
            'branch',
        ]

        read_only_fields = [
            'id',
            'retailer',
            'branch',
        ]


# ================= CREATE STAFF ================= #

class CreateStaffSerializer(
    serializers.ModelSerializer
):

    password = serializers.CharField(
        write_only=True
    )

    role = serializers.CharField(
        required=False,
        default="staff"
    )

    class Meta:

        model = User

        fields = [
            "username",
            "email",
            "password",
            "phone",
            "role",
        ]

    # =====================================================
    # VALIDATE USERNAME
    # =====================================================

    def validate_username(
        self,
        value
    ):

        if User.objects.filter(
            username=value
        ).exists():

            raise serializers.ValidationError(
                "Username already exists"
            )

        return value

    # =====================================================
    # VALIDATE EMAIL
    # =====================================================

    def validate_email(
        self,
        value
    ):

        if User.objects.filter(
            email=value
        ).exists():

            raise serializers.ValidationError(
                "Email already exists"
            )

        return value

    # =====================================================
    # VALIDATE PASSWORD
    # =====================================================

    def validate_password(
        self,
        value
    ):

        validate_password(value)

        return value

    # =====================================================
    # CREATE USER
    # =====================================================

    def create(
        self,
        validated_data
    ):

        request = self.context.get(
            "request"
        )

        role = validated_data.pop(
            "role",
            "staff"
        )

        # =====================================================
        # ROLE RESTRICTION
        # =====================================================

        allowed_roles = []

        # PLATFORM OWNER
        if request.user.is_superuser:

            allowed_roles = [
                "superadmin",
                "admin",
                "manager",
                "staff",
            ]

        # RETAILER SUPERADMIN
        elif request.user.role == "superadmin":

            allowed_roles = [
                "admin",
                "manager",
                "staff",
            ]

        # ADMIN
        elif request.user.role == "admin":

            allowed_roles = [
                "staff",
            ]

        # STAFF CANNOT CREATE USERS
        else:

            raise serializers.ValidationError({
                "error": (
                    "You do not have permission "
                    "to create users"
                )
            })

        # =====================================================
        # INVALID ROLE CHECK
        # =====================================================

        if role not in allowed_roles:

            raise serializers.ValidationError({
                "role": (
                    f"You cannot create "
                    f"{role} users"
                )
            })

        # =====================================================
        # RETAILER / BRANCH ASSIGNMENT
        # =====================================================

        retailer = validated_data.pop(
            "retailer",
            request.user.retailer
        )

        branch = validated_data.pop(
            "branch",
            request.user.branch
        )

        # =====================================================
        # CREATE USER
        # =====================================================

        user = User.objects.create_user(
            username=validated_data["username"],

            email=validated_data["email"],

            password=validated_data["password"],

            phone=validated_data.get(
                "phone"
            ),

            role=role,

            retailer=retailer,

            branch=branch,

            is_active=True,
        )

        # =====================================================
        # PASSWORD CHANGE TIME
        # =====================================================

        user.password_changed_at = now()

        user.save(
            update_fields=[
                "password_changed_at"
            ]
        )

        return user


# ================= LOGIN ================= #

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        try:
            user = User.objects.get(
                username=username
            )

        except User.DoesNotExist:

            raise serializers.ValidationError(
                "Invalid credentials"
            )

        # Check account lock
        if user.account_locked_until:

            if user.account_locked_until > timezone.now():

                raise serializers.ValidationError(
                    f"Account is locked until "
                    f"{user.account_locked_until.strftime('%d-%m-%Y %H:%M')}"
                )

        # Authenticate user
        user = authenticate(
            username=username,
            password=password
        )

        if not user:

            db_user = User.objects.filter(
                username=username
            ).first()

            if db_user:

                db_user.failed_login_attempts += 1

                if db_user.failed_login_attempts >= 4:

                    db_user.account_locked_until = (
                        timezone.now() +
                        timedelta(minutes=30)
                    )

                db_user.save(
                    update_fields=[
                        "failed_login_attempts",
                        "account_locked_until"
                    ]
                )

            raise serializers.ValidationError(
                "Invalid credentials"
            )

        if not user.is_active:

            raise serializers.ValidationError(
                "Account is inactive"
            )

        if getattr(user, "is_deleted", False):

            raise serializers.ValidationError(
                "Account has been deleted"
            )

        # Reset failed attempts after successful login
        user.failed_login_attempts = 0
        user.account_locked_until = None

        user.save(
            update_fields=[
                "failed_login_attempts",
                "account_locked_until"
            ]
        )

        return user 

# ================= VERIFY OTP ================= #

class VerifyOTPSerializer(serializers.Serializer):

    user_id = serializers.IntegerField()

    otp = serializers.CharField(
        max_length=6,
        min_length=6
    )

    def validate(self, data):

        try:
            user = User.objects.get(
                id=data["user_id"]
            )

        except User.DoesNotExist:

            raise serializers.ValidationError(
                "Invalid user"
            )

        data["user"] = user

        return data
    
# ================= RESEND OTP ================= #

class ResendOTPSerializer(serializers.Serializer):

    user_id = serializers.IntegerField()

    def validate_user_id(self, value):

        if not User.objects.filter(
            id=value
        ).exists():

            raise serializers.ValidationError(
                "User not found"
            )

        return value
    

# ================= ADMIN RESET PASSWORD ================= #

class AdminResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()

    new_password = serializers.CharField(
        write_only=True
    )

    def validate(self, data):
        request = self.context.get('request')

        try:
            user = User.objects.get(
                username=data['username']
            )

        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User not found"
            )

        # ================= SUPER ADMIN ================= #

        if request.user.is_superuser or request.user.role == "superadmin":
            pass

        # ================= ADMIN RULES ================= #

        else:

            if user == request.user:
                raise serializers.ValidationError(
                    "You cannot reset your own password"
                )

            if user.role != 'staff':
                raise serializers.ValidationError(
                    "You can only reset staff passwords"
                )

            # ================= RETAILER SECURITY ================= #

            if user.retailer != request.user.retailer:
                raise serializers.ValidationError(
                    "You cannot access another retailer user"
                )

            # ================= BRANCH SECURITY ================= #

            if user.branch != request.user.branch:
                raise serializers.ValidationError(
                    "You cannot access another branch user"
                )

        validate_password(
            data['new_password']
        )

        data['user'] = user

        return data

    def save(self):
        user = self.validated_data['user']

        user.set_password(
            self.validated_data['new_password']
        )

        user.password_changed_at = now()

        user.save()

        return user