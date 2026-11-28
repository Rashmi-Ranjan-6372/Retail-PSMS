from django.contrib import admin

from .models import (
    ExpenseCategory,
    Expense,
    ExpenseAttachment,
)


# ==========================================================
#                  EXPENSE ATTACHMENT INLINE
# ==========================================================
class ExpenseAttachmentInline(admin.TabularInline):

    model = ExpenseAttachment
    extra = 0

    fields = (
        "file",
        "file_name",
        "uploaded_by",
        "uploaded_at",
    )

    readonly_fields = (
        "uploaded_by",
        "uploaded_at",
    )


# ==========================================================
#                  EXPENSE CATEGORY ADMIN
# ==========================================================
@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "scope",
        "retailer",
        "is_active",
        "created_by",
        "created_at",
    )

    list_filter = (
        "scope",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "retailer__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "scope",
        "name",
    )

    list_per_page = 25


# ==========================================================
#                      EXPENSE ADMIN
# ==========================================================
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "expense_number",
        "title",
        "scope",
        "retailer",
        "branch",
        "category",
        "amount",
        "tax_amount",
        "status",
        "expense_date",
        "created_by",
    )

    list_filter = (
        "scope",
        "status",
        "payment_method",
        "expense_date",
        "created_at",
    )

    search_fields = (
        "expense_number",
        "title",
        "description",
        "vendor_name",
        "invoice_number",
        "payment_reference",
        "retailer__name",
        "branch__name",
        "category__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "approved_at",
        "paid_at",
        "cancelled_at",
    )

    autocomplete_fields = (
        "retailer",
        "branch",
        "category",
        "created_by",
        "approved_by",
        "cancelled_by",
    )

    inlines = (ExpenseAttachmentInline,)

    fieldsets = (
        (
            "Expense Information",
            {
                "fields": (
                    "scope",
                    "retailer",
                    "branch",
                    "category",
                    "expense_number",
                    "title",
                    "description",
                    "expense_date",
                )
            },
        ),
        (
            "Amount and Payment",
            {
                "fields": (
                    "amount",
                    "tax_amount",
                    "payment_method",
                    "payment_reference",
                    "vendor_name",
                    "invoice_number",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                    "notes",
                )
            },
        ),
        (
            "Approval Details",
            {
                "fields": (
                    "created_by",
                    "approved_by",
                    "approved_at",
                    "paid_at",
                )
            },
        ),
        (
            "Cancellation Details",
            {
                "fields": (
                    "cancelled_by",
                    "cancelled_at",
                    "cancellation_reason",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    ordering = (
        "-expense_date",
        "-created_at",
    )

    list_per_page = 25


# ==========================================================
#                EXPENSE ATTACHMENT ADMIN
# ==========================================================
@admin.register(ExpenseAttachment)
class ExpenseAttachmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "expense",
        "file_name",
        "uploaded_by",
        "uploaded_at",
    )

    search_fields = (
        "file_name",
        "expense__expense_number",
        "expense__title",
    )

    readonly_fields = ("uploaded_at",)

    autocomplete_fields = (
        "expense",
        "uploaded_by",
    )

    ordering = ("-uploaded_at",)

    list_per_page = 25
