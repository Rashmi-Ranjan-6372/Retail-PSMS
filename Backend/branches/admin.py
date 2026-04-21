from django.contrib import admin
from django.utils.html import format_html
from .models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    # ================= LIST DISPLAY ================= #
    list_display = (
        'id',
        'name',
        'code',
        'logo_preview',   # ✅ logo in list
        'phone',
        'email',
        'is_active',
        'created_at',
        'deleted_at'
    )

    # ================= SEARCH ================= #
    search_fields = (
        'name',
        'code',
        'phone',
        'email',
        'address'
    )

    # ================= FILTER ================= #
    list_filter = (
        'is_active',
        'created_at',
    )

    # ================= ORDER ================= #
    ordering = ('name',)

    # ================= READONLY ================= #
    readonly_fields = (
        'logo_preview',   # ✅ show preview
        'created_at',
        'updated_at',
        'deleted_at',
        'deleted_by'
    )

    # ================= DATE ================= #
    date_hierarchy = 'created_at'

    # ================= FIELDSETS ================= #
    fieldsets = (
        ('Branch Information', {
            'fields': (
                'name',
                'code',
                'logo',           
                'logo_preview',  
                'address',
                'phone',
                'email',
                'license_number',
                'gst_number',
            )
        }),

        ('Status', {
            'fields': (
                'is_active',
            )
        }),

        ('Audit Information', {
            'fields': (
                'created_at',
                'updated_at',
                'deleted_at',
                'deleted_by',
            ),
            'classes': ('collapse',),
        }),
    )

    # ================= LOGO PREVIEW ================= #
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:8px;border:1px solid #ddd;" />',
                obj.logo.url
            )
        return "No Logo"

    logo_preview.short_description = "Logo"

    # ================= ACTIONS ================= #
    actions = ['soft_delete_branches', 'restore_branches']

    def soft_delete_branches(self, request, queryset):
        for branch in queryset:
            if branch.is_active:
                branch.soft_delete(request.user)

        self.message_user(request, "Selected branches deactivated successfully")

    soft_delete_branches.short_description = "Soft delete selected branches"

    def restore_branches(self, request, queryset):
        for branch in queryset:
            if not branch.is_active:
                branch.restore()

        self.message_user(request, "Selected branches restored successfully")

    restore_branches.short_description = "Restore selected branches"

    # ================= PERMISSIONS ================= #
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    # Remove default bulk delete
    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']

        return actions