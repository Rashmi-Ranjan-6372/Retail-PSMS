from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.timezone import make_aware
import datetime

class CustomJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        user = super().get_user(validated_token)

        token_iat = validated_token.get('iat')

        if user.password_changed_at and token_iat:
            token_time = make_aware(datetime.datetime.fromtimestamp(token_iat))

            if token_time < user.password_changed_at:
                raise AuthenticationFailed("Password changed. Please login again.")

        return user