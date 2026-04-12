from django.contrib import admin
from .models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'phone', 'email', 'created_at'
    )

    search_fields = (
        'name', 'phone', 'email', 'address'
    )

    list_filter = ('created_at',)
    ordering = ('name',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Branch Information', {
            'fields': (
                'name', 'address', 'phone', 'email'
            )
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )