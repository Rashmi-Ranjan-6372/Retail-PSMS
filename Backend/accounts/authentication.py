from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.timezone import make_aware, is_naive
import datetime


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication with enhanced security:
    - Checks if the user is active
    - Verifies account lock status
    - Invalidates tokens after password change
    """

    def get_user(self, validated_token):
        user = super().get_user(validated_token)

        # Ensure user exists
        if user is None:
            raise AuthenticationFailed(
                "User not found.",
                code="user_not_found"
            )

        # Check if user is active
        if not user.is_active:
            raise AuthenticationFailed(
                "User account is inactive.",
                code="user_inactive"
            )

        # Check if account is locked
        if hasattr(user, "is_account_locked") and user.is_account_locked():
            raise AuthenticationFailed(
                "Your account is locked. Please contact the administrator.",
                code="account_locked"
            )

        # Invalidate token if password has been changed
        token_iat = validated_token.get("iat")
        if user.password_changed_at and token_iat:
            try:
                token_time = datetime.datetime.fromtimestamp(token_iat)

                if is_naive(token_time):
                    token_time = make_aware(token_time)

                if token_time < user.password_changed_at:
                    raise AuthenticationFailed(
                        "Password changed. Please log in again.",
                        code="password_changed"
                    )
            except (TypeError, ValueError, OSError):
                raise AuthenticationFailed(
                    "Invalid token timestamp.",
                    code="invalid_token"
                )

        return user