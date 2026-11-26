from rest_framework import serializers

from .models import (
    PlatformEmailConfiguration,
    RetailerEmailConfiguration,
)
from .encryption import encrypt_password


class BaseEmailConfigurationSerializer(serializers.ModelSerializer):

    smtp_password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
        trim_whitespace=False,
    )

    password_configured = serializers.SerializerMethodField()

    class Meta:
        fields = [
            "id",
            "smtp_host",
            "smtp_port",
            "email_host_user",
            "smtp_password",
            "password_configured",
            "from_email",
            "use_tls",
            "use_ssl",
            "is_active",
            "is_verified",
            "last_tested_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "is_verified",
            "last_tested_at",
            "created_at",
            "updated_at",
            "password_configured",
        ]

    def get_password_configured(self, obj):
        return bool(obj.encrypted_email_host_password)

    def validate(self, attrs):

        use_tls = attrs.get(
            "use_tls",
            getattr(self.instance, "use_tls", False),
        )

        use_ssl = attrs.get(
            "use_ssl",
            getattr(self.instance, "use_ssl", False),
        )

        if use_tls and use_ssl:
            raise serializers.ValidationError(
                {"use_tls": "TLS and SSL cannot both be enabled."}
            )

        if (
            not 1
            <= attrs.get(
                "smtp_port",
                getattr(self.instance, "smtp_port", 587),
            )
            <= 65535
        ):
            raise serializers.ValidationError(
                {"smtp_port": "SMTP port must be between 1 and 65535."}
            )

        smtp_fields = {
            "smtp_host",
            "smtp_port",
            "email_host_user",
            "from_email",
            "use_tls",
            "use_ssl",
        }

        configuration_changed = False

        if self.instance:

            configuration_changed = any(
                field in attrs and getattr(self.instance, field) != attrs[field]
                for field in smtp_fields
            )

        password_changed = bool(attrs.get("smtp_password"))

        verification_invalidated = configuration_changed or password_changed

        if attrs.get("is_active") is True:

            if not self.instance:
                raise serializers.ValidationError(
                    {
                        "is_active": (
                            "Create and test the SMTP configuration "
                            "before activation."
                        )
                    }
                )

            if verification_invalidated:
                raise serializers.ValidationError(
                    {
                        "is_active": (
                            "SMTP configuration has changed. "
                            "Test the updated configuration before activation."
                        )
                    }
                )

            if not self.instance.is_verified:
                raise serializers.ValidationError(
                    {
                        "is_active": (
                            "Test the SMTP configuration successfully "
                            "before activation."
                        )
                    }
                )

        return attrs

    def create(self, validated_data):

        password = validated_data.pop("smtp_password", None)

        if not password:
            raise serializers.ValidationError(
                {"smtp_password": "SMTP password is required."}
            )

        validated_data["encrypted_email_host_password"] = encrypt_password(password)

        validated_data["is_verified"] = False
        validated_data["is_active"] = False

        return super().create(validated_data)

    def update(self, instance, validated_data):

        password = validated_data.pop("smtp_password", None)

        smtp_fields = {
            "smtp_host",
            "smtp_port",
            "email_host_user",
            "from_email",
            "use_tls",
            "use_ssl",
        }

        configuration_changed = any(
            field in validated_data
            and getattr(instance, field) != validated_data[field]
            for field in smtp_fields
        )

        if password or configuration_changed:

            instance.is_verified = False
            instance.is_active = False

            validated_data["is_verified"] = False
            validated_data["is_active"] = False

        if password:

            validated_data["encrypted_email_host_password"] = encrypt_password(password)

        return super().update(instance, validated_data)


class PlatformEmailConfigurationSerializer(BaseEmailConfigurationSerializer):

    class Meta(BaseEmailConfigurationSerializer.Meta):
        model = PlatformEmailConfiguration


class RetailerEmailConfigurationSerializer(BaseEmailConfigurationSerializer):

    class Meta(BaseEmailConfigurationSerializer.Meta):
        model = RetailerEmailConfiguration
