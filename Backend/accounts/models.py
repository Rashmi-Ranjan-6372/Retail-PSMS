from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from branches.models import Branch

class Retailer(models.Model):
    name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField(null=True, blank=True)
    gst_number = models.CharField(max_length=50, null=True, blank=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to="retailer_logos/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_retailers"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["mobile"]),
        ]

class RetailerBranchAutoFillMixin(models.Model):
    retailer = models.ForeignKey(
        Retailer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_set"
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_set"
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        if hasattr(self, "_current_user"):

            if not self.retailer:
                self.retailer = self._current_user.retailer

            if not self.branch:
                self.branch = self._current_user.branch

        super().save(*args, **kwargs)


class User(AbstractUser):
    ROLE_CHOICES = (
        ("superadmin", "Super Admin"),
        ("admin", "Admin"),
        ("pharmacist", "Pharmacist"),
        ("store_manager", "Store Manager"),
        ("cashier", "Cashier"),
        ("staff", "Staff"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="staff")
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    employee_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    license_number = models.CharField(max_length=100, blank=True, null=True)
    license_expiry = models.DateField(null=True, blank=True)

    retailer = models.ForeignKey(
        Retailer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="users"
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )
    password_changed_at = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    is_two_factor_enabled = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_users"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_user = User.objects.filter(pk=self.pk).first()

            if old_user and old_user.password != self.password:
                self.password_changed_at = timezone.now()

        super().save(*args, **kwargs)

    def is_account_locked(self):
        return (
            self.account_locked_until and
            self.account_locked_until > timezone.now()
        )

    def is_super_admin(self):
        return self.role == "superadmin" or self.is_superuser

    def is_admin(self):
        return self.role == "admin"

    def __str__(self):
        return f"{self.username} ({self.role})"

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["email"]),
            models.Index(fields=["role"]),
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["retailer", "branch"]),
            models.Index(fields=["retailer", "role"]),
            models.Index(fields=["retailer", "is_active"]),
        ]

        permissions = [
            ("can_manage_inventory", "Can manage inventory"),
            ("can_manage_sales", "Can manage sales"),
            ("can_manage_purchases", "Can manage purchases"),
            ("can_view_reports", "Can view reports"),
        ]

class LoginLog(RetailerBranchAutoFillMixin):
    STATUS_CHOICES = (
        ("success", "Success"),
        ("failed", "Failed"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="success"
    )

    def __str__(self):
        return f"{self.user} - {self.status} - {self.login_time}"

    class Meta:
        ordering = ["-login_time"]

        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["status"]),
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["login_time"]),
        ]


class UserSession(RetailerBranchAutoFillMixin):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    device_id = models.CharField(max_length=255)
    refresh_token = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    revoked_at = models.DateTimeField(null=True, blank=True)

    def revoke(self):
        self.is_active = False
        self.revoked_at = timezone.now()
        self.save(update_fields=["is_active", "revoked_at"])

    def __str__(self):
        return f"{self.user} - {self.device_id} - Active: {self.is_active}"

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["refresh_token"]),
        ]

class AuditLog(RetailerBranchAutoFillMixin):
    ACTION_CHOICES = (
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
        ("login", "Login"),
        ("logout", "Logout"),
        ("view", "View"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=255)
    object_id = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if self.user:

            if not self.retailer:
                self.retailer = self.user.retailer

            if not self.branch:
                self.branch = self.user.branch

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name}"

    class Meta:
        ordering = ["-timestamp"]

        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["action"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["retailer"]),
            models.Index(fields=["timestamp"]),
        ]