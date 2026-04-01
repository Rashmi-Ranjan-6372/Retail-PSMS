from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import LoginLog, User, UserSession


# ================= USER ADMIN ================= #
@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'id', 'username', 'email', 'role',
        'is_active', 'is_staff',
        'created_at', 'password_changed_at'
    )

    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')

    search_fields = ('username', 'email', 'phone')

    ordering = ('-created_at',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('email', 'phone')
        }),
        ('Role & Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'created_at', 'updated_at', 'password_changed_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'role', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at', 'password_changed_at')


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

    readonly_fields = (
        'login_time', 'logout_time',
        'ip_address', 'user_agent', 'status'
    )


# ================= USER SESSION ADMIN ================= #
@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'user', 'device_id',
        'ip_address', 'is_active',
        'created_at', 'last_activity'
    )

    list_filter = ('is_active', 'created_at')

    search_fields = ('user__username', 'device_id', 'ip_address')

    ordering = ('-created_at',)

    readonly_fields = (
        'user', 'device_id', 'refresh_token',
        'ip_address', 'user_agent',
        'created_at', 'last_activity'
    )

    # 🔥 ACTION: Force logout selected sessions
    actions = ['force_logout']

    def force_logout(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected sessions logged out successfully.")

    force_logout.short_description = "Force logout selected sessions"