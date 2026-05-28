from django.contrib import admin

from settings.models.general_setting_models import (
    GeneralSetting
)

from settings.models.financial_year_models import (
    FinancialYear
)


# =========================
# GENERAL SETTINGS ADMIN
# =========================

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
        "created_at",
    )

    search_fields = (
        "retailer__name",
    )

    list_filter = (
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


# =========================
# FINANCIAL YEAR ADMIN
# =========================

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
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )