from django.contrib import admin
from masters.models import Supplier, Manufacturer

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "get_branches",
        "phone",
        "gst_no",
        "city",
        "state",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "state",
        "city",
        "created_at",
        "branches",
    )

    search_fields = ("name", "phone", "gst_no")

    ordering = ("-id",)

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "contact_person", "branches")
        }),
        ("Contact Info", {
            "fields": ("phone", "alternate_phone", "email")
        }),
        ("Legal Info", {
            "fields": ("gst_no", "drug_license_no")
        }),
        ("Address", {
            "fields": ("address", "city", "state", "pincode")
        }),
        ("Finance", {
            "fields": ("opening_balance",)
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields = [f for f in fields if f != "branches"]
        return fields

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not request.user.is_superuser:
            obj.branches.set([request.user.branch])

    def get_branches(self, obj):
        return ", ".join([b.name for b in obj.branches.all()])

    get_branches.short_description = "Branches"



@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "is_active",
        "created_at",
    )

    search_fields = ("name",)

    list_filter = ("is_active", "created_at")

    ordering = ("name",)

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Basic Info", {
            "fields": ("name",)
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )