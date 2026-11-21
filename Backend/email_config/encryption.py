from cryptography.fernet import Fernet
from django.core.exceptions import ImproperlyConfigured
from decouple import config


def get_fernet():

    key = config("SMTP_ENCRYPTION_KEY", default="")

    if not key:
        raise ImproperlyConfigured("SMTP_ENCRYPTION_KEY is missing.")

    try:
        return Fernet(key.encode())

    except Exception as exc:
        raise ImproperlyConfigured("SMTP_ENCRYPTION_KEY is invalid.") from exc


def encrypt_password(password):

    if not password:
        raise ValueError("SMTP password is required.")

    return get_fernet().encrypt(password.encode()).decode()


def decrypt_password(encrypted_password):

    if not encrypted_password:
        raise ValueError("SMTP password is not configured.")

    return get_fernet().decrypt(encrypted_password.encode()).decode()
