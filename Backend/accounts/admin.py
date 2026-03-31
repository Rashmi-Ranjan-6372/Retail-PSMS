from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import LoginLog, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    # Fields shown in list view
    list_display = ('id', 'username', 'email', 'role', 'is_active', 'is_staff', 'created_at', 'password_changed_at')

    # Filters on right side
    list_filter = ('role', 'is_active', 'is_staff')

    # Search bar
    search_fields = ('username', 'email', 'phone')

    # Default ordering
    ordering = ('-created_at',)

    # Field grouping in admin form
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
            'fields': ('last_login', 'created_at', 'updated_at')
        }),
    )

    # Fields when creating user from admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'role', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'login_time', 'logout_time', 'ip_address')
    list_filter = ('user', 'login_time')
    search_fields = ('user__username', 'ip_address')
    ordering = ('-login_time',)

    readonly_fields = ('login_time', 'logout_time', 'ip_address', 'user_agent')