from django.contrib import admin
from django.utils.html import format_html
from .models import Branch

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'retailer', 'name', 'code', 'logo_preview', 'phone', 'email', 'is_active', 'created_at', 'deleted_at')
    search_fields = ('name', 'code', 'phone', 'email', 'address', 'retailer__name')
    list_filter = ('retailer', 'is_active', 'created_at')
    ordering = ('name',)
    readonly_fields = ('logo_preview', 'created_at', 'updated_at', 'deleted_at', 'deleted_by')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Retailer Information', {
            'fields': ('retailer',)
        }),
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
            'fields': ('is_active',)
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

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:8px;border:1px solid #ddd;" />',
                obj.logo.url
            )
        return "No Logo"

    logo_preview.short_description = "Logo"

    actions = [
        'soft_delete_branches',
        'restore_branches',
        'activate_branches',
        'deactivate_branches',
    ]

    def soft_delete_branches(self, request, queryset):
        for branch in queryset:
            if branch.is_active:
                branch.soft_delete(request.user)
        self.message_user(request, "Selected branches soft deleted successfully")

    soft_delete_branches.short_description = "Soft delete selected branches"

    def restore_branches(self, request, queryset):
        for branch in queryset:
            if not branch.is_active:
                branch.restore()
        self.message_user(request, "Selected branches restored successfully")

    restore_branches.short_description = "Restore selected branches"

    def activate_branches(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} branches activated successfully")

    activate_branches.short_description = "Activate selected branches"

    def deactivate_branches(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} branches deactivated successfully")

    deactivate_branches.short_description = "Deactivate selected branches"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('retailer', 'deleted_by')

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if hasattr(request.user, "retailer"):
                obj.retailer = request.user.retailer
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions