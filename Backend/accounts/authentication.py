from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.timezone import make_aware, is_naive
from django.utils import timezone
import datetime


class CustomJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        user = super().get_user(validated_token)

        if user is None:
            raise AuthenticationFailed(
                "User not found.",
                code="user_not_found"
            )

        if not user.is_active:
            raise AuthenticationFailed(
                "User account is inactive.",
                code="user_inactive"
            )

        if getattr(user, "is_deleted", False):
            raise AuthenticationFailed(
                "User account has been deleted.",
                code="user_deleted"
            )

        if hasattr(user, "is_account_locked") and user.is_account_locked():
            raise AuthenticationFailed(
                "Your account is locked. Please contact administrator.",
                code="account_locked"
            )

        token_iat = validated_token.get("iat")

        if user.password_changed_at and token_iat:
            try:
                token_time = datetime.datetime.fromtimestamp(
                    token_iat,
                    tz=datetime.timezone.utc
                )

                if is_naive(token_time):
                    token_time = make_aware(token_time)

                password_changed_at = user.password_changed_at

                if timezone.is_naive(password_changed_at):
                    password_changed_at = make_aware(password_changed_at)

                if token_time < password_changed_at:
                    raise AuthenticationFailed(
                        "Password changed. Please login again.",
                        code="password_changed"
                    )

            except (
                TypeError,
                ValueError,
                OSError,
            ):
                raise AuthenticationFailed(
                    "Invalid token timestamp.",
                    code="invalid_token"
                )

        return user