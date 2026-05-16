from django.contrib import admin
from masters.models import (
    Supplier,
    Manufacturer,
    Category,
    Product,
    SalesOffer,
    Customer
)


# =========================================================
# BASE ADMIN
# =========================================================

class BaseRetailerBranchAdmin(admin.ModelAdmin):

    readonly_fields = ("created_at", "updated_at")

    def save_model(self, request, obj, form, change):

        if not request.user.is_superuser:

            if hasattr(obj, "retailer"):
                obj.retailer = request.user.retailer

            if hasattr(obj, "branch") and not obj.branch:
                obj.branch = request.user.branch

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        if hasattr(self.model, "retailer"):
            qs = qs.filter(retailer=request.user.retailer)

        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if not request.user.is_superuser:

            if db_field.name == "retailer":
                kwargs["queryset"] = db_field.related_model.objects.filter(
                    id=request.user.retailer_id
                )

            if db_field.name == "branch":
                kwargs["queryset"] = db_field.related_model.objects.filter(
                    retailer=request.user.retailer
                )

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):

        if not request.user.is_superuser:

            if db_field.name == "branches":
                kwargs["queryset"] = db_field.related_model.objects.filter(
                    retailer=request.user.retailer
                )

        return super().formfield_for_manytomany(
            db_field,
            request,
            **kwargs
        )


# =========================================================
# SUPPLIER ADMIN
# =========================================================

@admin.register(Supplier)
class SupplierAdmin(BaseRetailerBranchAdmin):

    list_display = (
        "id",
        "name",
        "retailer",
        "get_branches",
        "phone",
        "gst_no",
        "city",
        "state",
        "is_active",
        "created_at",
    )

    list_filter = (
        "retailer",
        "is_active",
        "state",
        "city",
        "created_at",
        "branches",
    )

    search_fields = (
        "name",
        "phone",
        "gst_no",
    )

    ordering = ("-id",)

    fieldsets = (
        ("Retailer Info", {
            "fields": (
                "retailer",
                "branches",
            )
        }),

        ("Basic Info", {
            "fields": (
                "name",
                "contact_person",
            )
        }),

        ("Contact Info", {
            "fields": (
                "phone",
                "alternate_phone",
                "email",
            )
        }),

        ("Legal Info", {
            "fields": (
                "gst_no",
                "drug_license_no",
            )
        }),

        ("Address", {
            "fields": (
                "address",
                "city",
                "state",
                "pincode",
            )
        }),

        ("Finance", {
            "fields": (
                "opening_balance",
            )
        }),

        ("Status", {
            "fields": (
                "is_active",
            )
        }),

        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    def save_model(self, request, obj, form, change):

        super().save_model(request, obj, form, change)

        if not request.user.is_superuser:
            obj.branches.set([request.user.branch])

    def get_branches(self, obj):
        return ", ".join(
            [branch.name for branch in obj.branches.all()]
        )

    get_branches.short_description = "Branches"


# =========================================================
# MANUFACTURER ADMIN
# =========================================================

@admin.register(Manufacturer)
class ManufacturerAdmin(BaseRetailerBranchAdmin):

    list_display = (
        "id",
        "name",
        "retailer",
        "is_active",
        "created_at",
    )

    search_fields = ("name",)

    list_filter = (
        "retailer",
        "is_active",
        "created_at",
    )

    ordering = ("name",)

    fieldsets = (
        ("Retailer Info", {
            "fields": (
                "retailer",
            )
        }),

        ("Basic Info", {
            "fields": (
                "name",
            )
        }),

        ("Status", {
            "fields": (
                "is_active",
            )
        }),

        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


# =========================================================
# CATEGORY ADMIN
# =========================================================

@admin.register(Category)
class ProductCategoryAdmin(BaseRetailerBranchAdmin):

    list_display = (
        "id",
        "name",
        "code",
        "retailer",
        "is_active",
        "created_at",
    )

    list_filter = (
        "retailer",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
    )

    ordering = ("name",)

    fields = (
        "retailer",
        "name",
        "code",
        "description",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_per_page = 20

    def save_model(self, request, obj, form, change):

        if obj.code:
            obj.code = obj.code.upper()

        super().save_model(request, obj, form, change)


# =========================================================
# PRODUCT ADMIN
# =========================================================

@admin.register(Product)
class ProductAdmin(BaseRetailerBranchAdmin):

    list_display = (
        "id",
        "name",
        "retailer",
        "category",
        "manufacturer",
        "strength",
        "units_per_strip",
        "minimum_stock",
        "is_active",
        "created_at",
    )

    list_filter = (
        "retailer",
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

    ordering = ("name",)

    fieldsets = (

        ("Retailer Info", {
            "fields": (
                "retailer",
            )
        }),

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


# =========================================================
# SALES OFFER ADMIN
# =========================================================

@admin.register(SalesOffer)
class SalesOfferAdmin(BaseRetailerBranchAdmin):

    list_display = (
        "id",
        "name",
        "retailer",
        "branch",
        "offer_type",
        "discount_type",
        "start_date",
        "end_date",
        "is_active",
    )

    list_filter = (
        "retailer",
        "branch",
        "offer_type",
        "discount_type",
        "is_active",
    )

    search_fields = (
        "name",
        "member_type",
    )

    ordering = ("-created_at",)

    fieldsets = (

        ("Retailer Info", {
            "fields": (
                "retailer",
                "branch",
            )
        }),

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


# =========================================================
# CUSTOMER ADMIN
# =========================================================

@admin.register(Customer)
class CustomerAdmin(BaseRetailerBranchAdmin):

    list_display = (
        "id",
        "name",
        "retailer",
        "branch",
        "mobile",
        "email",
        "is_active",
        "created_at",
    )

    list_filter = (
        "retailer",
        "branch",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "mobile",
        "email",
    )

    ordering = ("-created_at",)

    list_editable = ("is_active",)

    fields = (
        "retailer",
        "branch",
        "name",
        "mobile",
        "email",
        "address",
        "is_active",
        "created_at",
        "updated_at",
    )