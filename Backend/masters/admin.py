from django.contrib import admin
from masters.models import Supplier, Manufacturer, Category, Product, SalesOffer
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

@admin.register(Category)
class ProductCategoryAdmin(admin.ModelAdmin):
    
    # ================= LIST VIEW ================= #
    list_display = (
        "id",
        "name",
        "code",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
    )

    ordering = ("name",)
    fields = (
        "name",
        "code",
        "description",
        "is_active",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_per_page = 20
    def save_model(self, request, obj, form, change):
        if obj.code:
            obj.code = obj.code.upper()
        super().save_model(request, obj, form, change)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "category",
        "manufacturer",
        "strength",
        "units_per_strip",
        "loose_sale_allowed",
        "prescription_required",
        "minimum_stock",
        "is_active",
        "created_at",
    )

    list_filter = (
        "category",
        "manufacturer",
        "loose_sale_allowed",
        "prescription_required",
        "is_active",
    )

    search_fields = (
        "name",
        "strength",
        "rack_no",
    )

    ordering = (
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "name",
                "category",
                "manufacturer",
                "strength",
            )
        }),

        ("Stock Settings", {
            "fields": (
                "units_per_strip",
                "minimum_stock",
                "rack_no",
            )
        }),

        ("Sales Settings", {
            "fields": (
                "loose_sale_allowed",
                "prescription_required",
            )
        }),

        ("Status", {
            "fields": (
                "is_active",
                "deleted_at",
            )
        }),

        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

@admin.register(SalesOffer)
class SalesOfferAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "offer_type",
        "discount_type",
        "discount_percentage",
        "flat_discount_amount",
        "start_date",
        "end_date",
        "is_active",
        "created_at",
    )

    list_filter = (
        "offer_type",
        "discount_type",
        "is_active",
        "start_date",
        "end_date",
    )

    search_fields = (
        "name",
        "member_type",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "name",
                "offer_type",
                "discount_type",
            )
        }),

        ("Offer Target", {
            "fields": (
                "product",
                "category",
                "manufacturer",
            )
        }),

        ("Discount Details", {
            "fields": (
                "discount_percentage",
                "flat_discount_amount",
            )
        }),

        ("Buy X Get Y", {
            "fields": (
                "buy_quantity",
                "free_quantity",
            )
        }),

        ("Quantity / Bill Conditions", {
            "fields": (
                "minimum_quantity",
                "minimum_bill_amount",
            )
        }),

        ("Special Offers", {
            "fields": (
                "expiry_before_days",
                "member_type",
            )
        }),

        ("Validity", {
            "fields": (
                "start_date",
                "end_date",
                "is_active",
            )
        }),

        ("Extra", {
            "fields": (
                "deleted_at",
                "created_at",
                "updated_at",
            )
        }),
    )