import logging

from django.core.mail import EmailMessage, get_connection
from django.core.exceptions import ImproperlyConfigured

from email_config.models import (
    PlatformEmailConfiguration,
    RetailerEmailConfiguration,
)
from email_config.encryption import decrypt_password

logger = logging.getLogger(__name__)


# ============================================================
# SMTP CONNECTION
# ============================================================


def get_smtp_connection(configuration):

    if not configuration.is_active:
        raise ImproperlyConfigured("SMTP configuration is inactive.")

    if not configuration.is_verified:
        raise ImproperlyConfigured("SMTP configuration has not been verified.")

    password = decrypt_password(configuration.encrypted_email_host_password)

    return get_connection(
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


# ============================================================
# COMMON EMAIL SENDING FUNCTION
# ============================================================


def send_configured_email(
    configuration,
    subject,
    message,
    recipient_list,
    html_message=None,
):

    if not recipient_list:
        raise ValueError("At least one recipient is required.")

    connection = get_smtp_connection(configuration)

    try:
        email = EmailMessage(
            subject=subject,
            body=html_message if html_message else message,
            from_email=configuration.from_email,
            to=recipient_list,
            connection=connection,
        )

        if html_message:
            email.content_subtype = "html"

        return email.send(fail_silently=False)

    except Exception:
        logger.exception("SMTP email sending failed.")
        raise

    finally:
        connection.close()


# ============================================================
# RETAILER EMAIL
# ============================================================


def send_retailer_email(
    retailer,
    subject,
    message,
    recipient_list,
    html_message=None,
):

    configuration = RetailerEmailConfiguration.objects.filter(retailer=retailer).first()

    if not configuration:
        raise ImproperlyConfigured("This retailer has not configured SMTP.")

    return send_configured_email(
        configuration=configuration,
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        html_message=html_message,
    )


# ============================================================
# PLATFORM OWNER EMAIL
# ============================================================


def send_platform_email(
    subject,
    message,
    recipient_list,
    html_message=None,
):

    configuration = PlatformEmailConfiguration.objects.filter(pk=1).first()

    if not configuration:
        raise ImproperlyConfigured("Platform SMTP configuration is missing.")

    return send_configured_email(
        configuration=configuration,
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        html_message=html_message,
    )


# ============================================================
# AUTHENTICATION EMAIL ROUTING
# ============================================================


def send_user_auth_email(
    user,
    subject,
    message,
    recipient_list,
    html_message=None,
):

    if user.is_superuser or getattr(user, "role", None) == "platform_owner":

        return send_platform_email(
            subject=subject,
            message=message,
            recipient_list=recipient_list,
            html_message=html_message,
        )

    retailer = getattr(user, "retailer", None)

    if not retailer:

        return send_platform_email(
            subject=subject,
            message=message,
            recipient_list=recipient_list,
            html_message=html_message,
        )

    configuration = RetailerEmailConfiguration.objects.filter(retailer=retailer).first()

    if configuration and configuration.is_active and configuration.is_verified:

        return send_retailer_email(
            retailer=retailer,
            subject=subject,
            message=message,
            recipient_list=recipient_list,
            html_message=html_message,
        )

    return send_platform_email(
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        html_message=html_message,
    )
