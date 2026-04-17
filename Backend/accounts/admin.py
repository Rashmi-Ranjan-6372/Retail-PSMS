from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import LoginLog, User, UserSession

# ================= USER ADMIN ================= #
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'branch', 'email', 'role',
        'is_active', 'is_staff', 'is_superuser',
        'created_at', 'password_changed_at'
    )

    list_filter = (
        'role', 'is_active', 'is_staff',
        'is_superuser', 'created_at'
    )

    search_fields = ('username', 'email', 'phone')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    readonly_fields = (
        'created_at', 'updated_at',
        'password_changed_at', 'last_login',
        'last_login_ip'
    )

    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'password')
        }),
        ('Personal Information', {
            'fields': (
                'first_name', 'last_name',
                'email', 'phone', 'branch'
            )
        }),
        ('Role & Permissions', {
            'fields': (
                'role', 'is_active', 'is_staff',
                'is_superuser', 'groups', 'user_permissions'
            )
        }),
        ('Security Information', {
            'classes': ('collapse',),
            'fields': (
                'last_login_ip',
                'password_changed_at',
            )
        }),
        ('Important Dates', {
            'fields': (
                'last_login', 'created_at', 'updated_at'
            )
        }),
    )

    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'phone',
                'branch', 'role',
                'password1', 'password2',
                'is_active', 'is_staff'
            ),
        }),
    )

    actions = ['activate_users', 'deactivate_users']

    @admin.action(description="Activate selected users")
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected users activated successfully.")

    @admin.action(description="Deactivate selected users")
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected users deactivated successfully.")


# ================= LOGIN LOG ADMIN ================= #
@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'status',
        'login_time', 'logout_time', 'ip_address'
    )

    list_filter = ('status', 'login_time', 'user')
    search_fields = ('user__username', 'ip_address')
    ordering = ('-login_time',)
    date_hierarchy = 'login_time'

    readonly_fields = (
        'login_time', 'logout_time',
        'ip_address', 'user_agent', 'status', 'user'
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# ================= USER SESSION ADMIN ================= #
@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'device_id',
        'ip_address', 'is_active',
        'created_at', 'last_activity',
        'masked_refresh_token'
    )

    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'device_id', 'ip_address')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    readonly_fields = (
        'user', 'device_id', 'refresh_token',
        'ip_address', 'user_agent',
        'created_at', 'last_activity',
        'masked_refresh_token'
    )

    actions = ['force_logout']

    def masked_refresh_token(self, obj):
        """Display a masked version of the refresh token."""
        if obj.refresh_token:
            return format_html(
                "<span title='Hidden for security'>****{}</span>",
                obj.refresh_token[-6:]
            )
        return "-"
    masked_refresh_token.short_description = "Refresh Token"

    @admin.action(description="Force logout selected sessions")
    def force_logout(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(
            request,
            "Selected sessions logged out successfully."
        )

    def has_add_permission(self, request):
        return False