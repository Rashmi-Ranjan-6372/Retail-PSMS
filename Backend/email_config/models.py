
from django.db import models
from django.core.exceptions import ValidationError


class BaseEmailConfiguration(models.Model):

    smtp_host = models.CharField(max_length=255)
    smtp_port = models.PositiveIntegerField(default=587)
    email_host_user = models.EmailField()
    encrypted_email_host_password = models.TextField()
    from_email = models.EmailField()
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    last_tested_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def clean(self):
        if self.use_tls and self.use_ssl:
            raise ValidationError(
                "TLS and SSL cannot both be enabled."
            )

        if not 1 <= self.smtp_port <= 65535:
            raise ValidationError(
                "SMTP port must be between 1 and 65535."
            )

    def __str__(self):
        return self.email_host_user


class PlatformEmailConfiguration(BaseEmailConfiguration):

    class Meta:
        verbose_name = "Platform Email Configuration"
        verbose_name_plural = "Platform Email Configuration"

    def save(self, *args, **kwargs):
        self.pk = 1
        self.full_clean()
        super().save(*args, **kwargs)


class RetailerEmailConfiguration(BaseEmailConfiguration):

    retailer = models.OneToOneField("accounts.Retailer",on_delete=models.CASCADE,related_name="email_configuration")

    class Meta:
        ordering = ["retailer__name"]

    def __str__(self):
        return f"{self.retailer.name} - {self.email_host_user}"
