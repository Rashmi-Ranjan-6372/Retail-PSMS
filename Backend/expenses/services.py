
from django.db import transaction
from django.utils import timezone

from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError,
)

from .models import Expense


# ==========================================================
#                    EXPENSE STATUS
# ==========================================================
DRAFT = "draft"
APPROVED = "approved"
PAID = "paid"
CANCELLED = "cancelled"


# ==========================================================
#                    USER ROLE HELPERS
# ==========================================================
def is_platform_owner(user):
    return (
        user.is_authenticated
        and user.is_active
        and (
            user.is_superuser
            or getattr(user, "role", None) == "platform_owner"
        )
    )


def get_user_role(user):
    return getattr(user, "role", None)


# ==========================================================
#                 EXPENSE ACCESS VALIDATION
# ==========================================================
def validate_expense_access(user, expense):

    if not user.is_authenticated or not user.is_active:
        raise PermissionDenied("You are not authorized to access expenses.")

    # Platform Owner can access platform expenses only.
    if is_platform_owner(user):

        if expense.scope != "platform":
            raise PermissionDenied(
                "You cannot access retailer expenses."
            )

        return

    # Retailer users cannot access platform expenses.
    if expense.scope != "retailer":
        raise PermissionDenied(
            "You cannot access platform expenses."
        )

    if not getattr(user, "retailer_id", None):
        raise PermissionDenied(
            "You are not associated with any retailer."
        )

    # Retailer ownership validation.
    if expense.retailer_id != user.retailer_id:
        raise PermissionDenied(
            "You cannot access another retailer's expense."
        )

    role = get_user_role(user)

    # Superadmin and Admin can access all retailer branches.
    if role in ("superadmin", "admin"):
        return

    # Other users can access only their assigned branch.
    user_branch_id = getattr(user, "branch_id", None)

    if not user_branch_id:
        raise PermissionDenied(
            "You are not assigned to any branch."
        )

    if expense.branch_id != user_branch_id:
        raise PermissionDenied(
            "You cannot access another branch's expense."
        )


# ==========================================================
#                EXPENSE ACTION PERMISSIONS
# ==========================================================
def validate_approval_permission(user, expense):

    validate_expense_access(user, expense)

    if is_platform_owner(user):
        return

    if get_user_role(user) not in ("superadmin", "admin"):
        raise PermissionDenied(
            "You do not have permission to approve expenses."
        )


def validate_payment_permission(user, expense):

    validate_expense_access(user, expense)

    if is_platform_owner(user):
        return

    if get_user_role(user) not in (
        "superadmin",
        "admin",
        "cashier",
    ):
        raise PermissionDenied(
            "You do not have permission to record expense payments."
        )


def validate_cancellation_permission(user, expense):

    validate_expense_access(user, expense)

    if is_platform_owner(user):
        return

    if get_user_role(user) not in ("superadmin", "admin"):
        raise PermissionDenied(
            "You do not have permission to cancel expenses."
        )


# ==========================================================
#                  GET LOCKED EXPENSE
# ==========================================================
def get_locked_expense(expense_id):

    try:
        return Expense.objects.select_for_update().get(
            id=expense_id
        )

    except Expense.DoesNotExist:
        raise ValidationError(
            {"expense": "Expense does not exist."}
        )


# ==========================================================
#                    APPROVE EXPENSE
# ==========================================================
@transaction.atomic
def approve_expense(*, expense_id, user):

    expense = get_locked_expense(expense_id)

    validate_approval_permission(user, expense)

    if expense.status != DRAFT:
        raise ValidationError(
            "Only draft expenses can be approved."
        )

    if expense.created_by_id == user.id:
        raise PermissionDenied(
            "You cannot approve an expense created by yourself."
        )

    expense.status = APPROVED
    expense.approved_by = user
    expense.approved_at = timezone.now()

    expense.full_clean()
    expense.save(
        update_fields=[
            "status",
            "approved_by",
            "approved_at",
            "updated_at",
        ]
    )

    return expense


# ==========================================================
#                    MARK EXPENSE PAID
# ==========================================================
@transaction.atomic
def mark_expense_paid(
    *,
    expense_id,
    user,
    payment_method=None,
    payment_reference=None,
):

    expense = get_locked_expense(expense_id)

    validate_payment_permission(user, expense)

    if expense.status != APPROVED:
        raise ValidationError(
            "Only approved expenses can be marked as paid."
        )

    if not payment_method:
        raise ValidationError(
            {"payment_method": "Payment method is required."}
        )

    expense.payment_method = payment_method
    expense.payment_reference = payment_reference or ""
    expense.status = PAID
    expense.paid_at = timezone.now()

    expense.full_clean()
    expense.save(
        update_fields=[
            "payment_method",
            "payment_reference",
            "status",
            "paid_at",
            "updated_at",
        ]
    )

    return expense


# ==========================================================
#                    CANCEL EXPENSE
# ==========================================================
@transaction.atomic
def cancel_expense(
    *,
    expense_id,
    user,
    cancellation_reason,
):

    expense = get_locked_expense(expense_id)

    validate_cancellation_permission(user, expense)

    if expense.status == PAID:
        raise ValidationError(
            "Paid expenses cannot be cancelled directly. "
            "Use a reversal or refund process."
        )

    if expense.status == CANCELLED:
        raise ValidationError(
            "This expense is already cancelled."
        )

    if not cancellation_reason or not cancellation_reason.strip():
        raise ValidationError(
            {"cancellation_reason": "Cancellation reason is required."}
        )

    expense.status = CANCELLED
    expense.cancelled_by = user
    expense.cancelled_at = timezone.now()
    expense.cancellation_reason = cancellation_reason.strip()

    expense.full_clean()
    expense.save(
        update_fields=[
            "status",
            "cancelled_by",
            "cancelled_at",
            "cancellation_reason",
            "updated_at",
        ]
    )

    return expense
