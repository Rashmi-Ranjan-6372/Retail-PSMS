from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.utils.timezone import now
from django.contrib.auth.password_validation import validate_password


# ================= USER SERIALIZER ================= #
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone']


# ================= CREATE STAFF ================= #
class CreateStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone']

    def create(self, validated_data):
        validated_data['role'] = 'staff'
        user = User.objects.create_user(**validated_data)

        # Track password change time
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
            raise serializers.ValidationError("Invalid credentials")
        return user

# ================= ADMIN RESET PASSWORD ================= #
class AdminResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        request = self.context.get('request')

        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        # ================= SUPERUSER ACCESS ================= #
        if request.user.is_superuser:
            # Superuser can reset ANY password
            pass

        # ================= ADMIN RULES ================= #
        else:
            # ❌ Admin cannot reset own password
            if user == request.user:
                raise serializers.ValidationError(
                    "You cannot reset your own password"
                )

            # ❌ Admin can ONLY reset staff
            if user.role != 'staff':
                raise serializers.ValidationError(
                    "You can only reset staff passwords"
                )

        validate_password(data['new_password'])

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.password_changed_at = now()
        user.save()
        return user