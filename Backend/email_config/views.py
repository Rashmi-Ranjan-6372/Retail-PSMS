import logging

from django.core.mail import EmailMessage, get_connection
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Retailer

from .models import PlatformEmailConfiguration, RetailerEmailConfiguration

from .serializers import (
    PlatformEmailConfigurationSerializer,
    RetailerEmailConfigurationSerializer,
)

from .encryption import decrypt_password

logger = logging.getLogger(__name__)


def is_platform_owner(user):
    return user.is_authenticated and (
        user.is_superuser or user.role == "platform_owner"
    )


def is_retailer_superadmin(user):
    return (
        user.is_authenticated
        and user.role == "superadmin"
        and user.retailer_id is not None
        and user.is_active
        and not user.is_deleted
    )


def test_smtp(configuration, recipient_email):

    password = decrypt_password(configuration.encrypted_email_host_password)

    connection = get_connection(
        backend="django.core.mail.backends.smtp.EmailBackend",
        host=configuration.smtp_host,
        port=configuration.smtp_port,
        username=configuration.email_host_user,
        password=password,
        use_tls=configuration.use_tls,
        use_ssl=configuration.use_ssl,
        timeout=20,
        fail_silently=False,
    )

    email = EmailMessage(
        subject="PSMS SMTP Configuration Test",
        body=("Congratulations! Your SMTP configuration " "is working correctly."),
        from_email=configuration.from_email,
        to=[recipient_email],
        connection=connection,
    )

    try:
        sent = email.send(fail_silently=False)

        if sent != 1:
            raise Exception("Test email was not sent.")

        configuration.is_verified = True
        configuration.last_tested_at = timezone.now()
        configuration.save(
            update_fields=["is_verified", "last_tested_at", "updated_at"]
        )

        return True

    finally:
        connection.close()


class PlatformEmailConfigurationAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not is_platform_owner(request.user):
            return Response(
                {"success": False, "message": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        configuration = PlatformEmailConfiguration.objects.filter(pk=1).first()

        if not configuration:
            return Response(
                {
                    "success": True,
                    "message": "Platform SMTP configuration not found.",
                    "data": None,
                }
            )

        serializer = PlatformEmailConfigurationSerializer(configuration)

        return Response(
            {
                "success": True,
                "message": "Platform SMTP configuration retrieved successfully.",
                "data": serializer.data,
            }
        )

    def post(self, request):

        if not is_platform_owner(request.user):
            return Response(
                {"success": False, "message": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        configuration = PlatformEmailConfiguration.objects.filter(pk=1).first()

        serializer = PlatformEmailConfigurationSerializer(
            configuration, data=request.data
        )

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Platform SMTP configuration saved successfully. Please test it before activation.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK if configuration else status.HTTP_201_CREATED,
        )

    def put(self, request):

        if not is_platform_owner(request.user):
            return Response(
                {"success": False, "message": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        configuration = PlatformEmailConfiguration.objects.filter(pk=1).first()

        if not configuration:
            return Response(
                {"success": False, "message": "Platform SMTP configuration not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PlatformEmailConfigurationSerializer(
            configuration, data=request.data, partial=True
        )

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Platform SMTP configuration updated successfully.",
                "data": serializer.data,
            }
        )

    def delete(self, request):

        if not is_platform_owner(request.user):
            return Response(
                {"success": False, "message": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        configuration = PlatformEmailConfiguration.objects.filter(pk=1).first()

        if not configuration:
            return Response(
                {"success": False, "message": "Platform SMTP configuration not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        configuration.delete()

        return Response(
            {
                "success": True,
                "message": "Platform SMTP configuration deleted successfully.",
            }
        )


class RetailerEmailConfigurationAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not is_retailer_superadmin(request.user):
            return Response(
                {"success": False, "message": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        configuration = RetailerEmailConfiguration.objects.filter(
            retailer_id=request.user.retailer_id
        ).first()

        if not configuration:
            return Response(
                {
                    "success": True,
                    "message": "Retailer SMTP configuration not found.",
                    "data": None,
                }
            )

        serializer = RetailerEmailConfigurationSerializer(configuration)

        return Response(
            {
                "success": True,
                "message": "Retailer SMTP configuration retrieved successfully.",
                "data": serializer.data,
            }
        )

    def post(self, request):

        if not is_retailer_superadmin(request.user):
            return Response(
                {"success": False, "message": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        configuration = RetailerEmailConfiguration.objects.filter(
            retailer_id=request.user.retailer_id
        ).first()

        serializer = RetailerEmailConfigurationSerializer(
            configuration, data=request.data
        )

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(retailer=request.user.retailer)

        return Response(
            {
                "success": True,
                "message": "Retailer SMTP configuration saved successfully. Please test it before activation.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK if configuration else status.HTTP_201_CREATED,
        )

    def put(self, request):

        if not is_retailer_superadmin(request.user):
            return Response(
                {"success": False, "message": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        configuration = RetailerEmailConfiguration.objects.filter(
            retailer_id=request.user.retailer_id
        ).first()

        if not configuration:
            return Response(
                {"success": False, "message": "Retailer SMTP configuration not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RetailerEmailConfigurationSerializer(
            configuration, data=request.data, partial=True
        )

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Retailer SMTP configuration updated successfully.",
                "data": serializer.data,
            }
        )

    def delete(self, request):

        if not is_retailer_superadmin(request.user):
            return Response(
                {"success": False, "message": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        configuration = RetailerEmailConfiguration.objects.filter(
            retailer_id=request.user.retailer_id
        ).first()

        if not configuration:
            return Response(
                {"success": False, "message": "Retailer SMTP configuration not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        configuration.delete()

        return Response(
            {
                "success": True,
                "message": "Retailer SMTP configuration deleted successfully.",
            }
        )


class PlatformSMTPTestAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if not is_platform_owner(request.user):
            return Response(
                {"success": False, "message": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        configuration = PlatformEmailConfiguration.objects.filter(pk=1).first()

        if not configuration:
            return Response(
                {"success": False, "message": "Platform SMTP configuration not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        recipient = request.data.get("recipient_email") or request.user.email

        if not recipient:
            return Response(
                {"success": False, "message": "Please provide a recipient_email."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            test_smtp(configuration, recipient)

            return Response(
                {
                    "success": True,
                    "message": "Platform SMTP test email sent successfully. Configuration is verified.",
                }
            )

        except Exception:
            logger.exception("Platform SMTP test failed.")

            return Response(
                {
                    "success": False,
                    "message": "SMTP test failed. Check the host, port, credentials and email provider settings.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class RetailerSMTPTestAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if not is_retailer_superadmin(request.user):
            return Response(
                {"success": False, "message": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        configuration = RetailerEmailConfiguration.objects.filter(
            retailer_id=request.user.retailer_id
        ).first()

        if not configuration:
            return Response(
                {"success": False, "message": "Retailer SMTP configuration not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        recipient = request.data.get("recipient_email") or request.user.email

        if not recipient:
            return Response(
                {"success": False, "message": "Please provide a recipient_email."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            test_smtp(configuration, recipient)

            return Response(
                {
                    "success": True,
                    "message": "Retailer SMTP test email sent successfully. Configuration is verified.",
                }
            )

        except Exception:
            logger.exception("Retailer SMTP test failed.")

            return Response(
                {
                    "success": False,
                    "message": "SMTP test failed. Check the host, port, credentials and email provider settings.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
