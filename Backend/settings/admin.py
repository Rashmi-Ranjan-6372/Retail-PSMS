from django.contrib import admin

from settings.models.models import GeneralSetting, FinancialYear

# ==========================================
# GENERAL SETTINGS ADMIN
# ==========================================


@admin.register(GeneralSetting)
class GeneralSettingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "retailer",
        "currency",
        "timezone",
        "low_stock_limit",
        "enable_gst",
        "enable_barcode",
        "enable_expiry_alert",
        "enable_loose_sale",
        "enable_negative_stock",
        "created_at",
    )

    search_fields = ("retailer__name",)

    list_filter = (
        "currency",
        "timezone",
        "enable_gst",
        "enable_barcode",
        "enable_expiry_alert",
        "enable_loose_sale",
        "enable_negative_stock",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("retailer",)

    list_per_page = 25


# ==========================================
# FINANCIAL YEAR ADMIN
# ==========================================


@admin.register(FinancialYear)
class FinancialYearAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "retailer",
        "branch",
        "start_date",
        "end_date",
        "is_active",
        "created_by",
        "created_at",
    )

    search_fields = (
        "name",
        "retailer__name",
        "branch__name",
    )

    list_filter = (
        "is_active",
        "start_date",
        "end_date",
        "retailer",
        "branch",
    )

    readonly_fields = (
        "created_by",
        "created_at",
        "updated_at",
    )

    date_hierarchy = "start_date"

    ordering = ("-start_date", "-id")

    list_select_related = (
        "retailer",
        "branch",
        "created_by",
    )

    list_per_page = 25
