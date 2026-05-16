from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.utils.timezone import now
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from django.contrib.auth import get_user_model
from branches.models import Branch
from .models import Retailer

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
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if Retailer.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Retailer email already exists"
            )

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User email already exists"
            )

        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists"
            )

        return value

    def create(self, validated_data):

        retailer = Retailer.objects.create(
            name=validated_data["retailer_name"],
            owner_name=validated_data["owner_name"],
            mobile=validated_data["mobile"],
            email=validated_data["email"],
            address=validated_data.get("address"),
            gst_number=validated_data.get("gst_number"),
            license_number=validated_data.get("license_number"),
        )

        branch = Branch.objects.create(
            retailer=retailer,
            name=validated_data["branch_name"]
        )

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role="superadmin",
            retailer=retailer,
            branch=branch,
            is_staff=True,
            is_active=True
        )

        return {
            "retailer": retailer,
            "branch": branch,
            "user": user
        }

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

class CreateStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password',
            'phone',
        ]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        request = self.context.get("request")

        validated_data['role'] = 'staff'

        validated_data['retailer'] = request.user.retailer
        validated_data['branch'] = request.user.branch

        user = User.objects.create_user(
            **validated_data
        )

        user.password_changed_at = now()

        user.save()

        return user


# ================= LOGIN ================= #

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )

        if not user:
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

        if (
            hasattr(user, "is_account_locked") and
            user.is_account_locked()
        ):
            raise serializers.ValidationError(
                "Account is temporarily locked"
            )

        return user


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