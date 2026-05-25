from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from .models import UserSession


class SessionValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            jwt_auth = JWTAuthentication()
            header = jwt_auth.get_header(request)

            if header:
                raw_token = (
                    jwt_auth.get_raw_token(header)
                )
                validated_token = (
                    jwt_auth.get_validated_token(
                        raw_token
                    )
                )
                user_id = validated_token.get(
                    "user_id"
                )

                token = str(raw_token)

                session_exists = (
                    UserSession.objects.filter(
                        user_id=user_id,
                        is_active=True
                    ).exists()
                )

                if not session_exists:

                    return JsonResponse({
                        "success": False,
                        "message": (
                            "Session expired "
                            "or logged out"
                        )
                    }, status=401)

        except Exception:
            pass

        response = self.get_response(request)
        return response