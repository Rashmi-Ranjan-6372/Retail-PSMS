from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Retailer, User, LoginLog, UserSession, AuditLog


@admin.register(Retailer)
class RetailerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner_name", "mobile", "email", "is_active", "created_at")
    search_fields = ("name", "owner_name", "mobile", "email", "gst_number")
    list_filter = ("is_active", "created_at")
    ordering = ("-created_at",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "email", "role", "retailer", "branch", "is_active", "is_deleted")
    list_filter = ("role", "is_active", "is_deleted", "retailer", "branch")
    search_fields = ("username", "email", "phone", "employee_id")

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Business Info", {
            "fields": (
                "role",
                "phone",
                "address",
                "profile_picture",
                "employee_id",
                "joining_date",
                "date_of_birth",
                "license_number",
                "license_expiry",
                "retailer",
                "branch",
            )
        }),
        ("Security Info", {
            "fields": (
                "password_changed_at",
                "last_login_ip",
                "failed_login_attempts",
                "account_locked_until",
                "is_two_factor_enabled",
                "otp_secret",
                "is_deleted",
            )
        }),
    )

    readonly_fields = ("password_changed_at",)


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "retailer", "branch", "status", "ip_address", "login_time")
    list_filter = ("status", "retailer", "branch", "login_time")
    search_fields = ("user__username", "ip_address")
    readonly_fields = ("login_time",)
    ordering = ("-login_time",)


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "device_id", "retailer", "branch", "is_active", "created_at", "last_activity")
    list_filter = ("is_active", "retailer", "branch")
    search_fields = ("user__username", "device_id", "ip_address")
    readonly_fields = ("created_at", "last_activity")
    ordering = ("-created_at",)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "action", "model_name", "object_id", "retailer", "branch", "timestamp")
    list_filter = ("action", "model_name", "retailer", "branch", "timestamp")
    search_fields = ("user__username", "model_name", "object_id", "description")
    readonly_fields = ("timestamp",)
    ordering = ("-timestamp",)