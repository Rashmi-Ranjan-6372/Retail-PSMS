from django.contrib import admin
from .models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'code',
        'phone',
        'email',
        'is_active',
        'created_at',
        'deleted_at'
    )

    search_fields = (
        'name',
        'code',
        'phone',
        'email',
        'address'
    )

    list_filter = (
        'is_active',
        'created_at',
    )

    ordering = ('name',)

    readonly_fields = (
        'created_at',
        'updated_at',
        'deleted_at',
        'deleted_by'
    )

    date_hierarchy = 'created_at'

    # ================= FIELDSETS ================= #
    fieldsets = (
        ('Branch Information', {
            'fields': (
                'name',
                'code',
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

    # ================= DISABLE HARD DELETE ================= #
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    # Optional: prevent bulk delete action
    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']

        return actions