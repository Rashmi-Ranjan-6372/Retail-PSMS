from django.utils import timezone

from rest_framework.exceptions import (
    ValidationError,
    PermissionDenied,
)

from .models import RetailerSubscription

from branches.models import Branch
from accounts.models import User

# ==========================================================
# GET RETAILER SUBSCRIPTION
# ==========================================================


def get_subscription(retailer):

    if not retailer:
        return None

    return (
        RetailerSubscription.objects.select_related("plan", "retailer")
        .filter(retailer=retailer)
        .first()
    )


# ==========================================================
# CHECK SUBSCRIPTION ACTIVE
# ==========================================================


def is_subscription_active(retailer):

    subscription = get_subscription(retailer)

    if not subscription:
        return False

    return subscription.is_active()


# ==========================================================
# CHECK SUBSCRIPTION WRITE ACCESS
# ==========================================================


def check_subscription_write_access(retailer):

    subscription = get_subscription(retailer)

    if not subscription:

        raise PermissionDenied(
            "No subscription assigned to this retailer. "
            "Please contact the platform administrator."
        )

    today = timezone.localdate()

    if subscription.status == "suspended":

        raise PermissionDenied(
            "Your subscription is suspended. "
            "Please contact the platform administrator."
        )

    if subscription.status == "expired":

        raise PermissionDenied(
            "Your subscription has expired. " "Please renew your subscription."
        )

    if subscription.start_date > today:

        raise PermissionDenied("Your subscription has not started yet.")

    if subscription.expiry_date < today:

        raise PermissionDenied(
            "Your subscription has expired. " "Please renew your subscription."
        )

    if subscription.status != "active":

        raise PermissionDenied("Your subscription is not active.")

    return subscription


# ==========================================================
# GET CURRENT BRANCH COUNT
# ==========================================================


def get_current_branch_count(retailer):

    return Branch.objects.filter(retailer=retailer, deleted_at__isnull=True).count()


# ==========================================================
# VALIDATE BRANCH SUBSCRIPTION LIMIT
# ==========================================================


def validate_branch_subscription(retailer):

    subscription = check_subscription_write_access(retailer)

    max_branches = subscription.plan.max_branches


    if max_branches == 0:
        return subscription

    current_branches = get_current_branch_count(retailer)

    if current_branches >= max_branches:

        raise ValidationError(
            {
                "subscription": (
                    f"Branch limit reached. "
                    f"Your current plan allows a maximum of "
                    f"{max_branches} branches."
                )
            }
        )

    return subscription


# ==========================================================
# GET CURRENT USER COUNT
# ==========================================================


def get_current_user_count(retailer):

    return User.objects.filter(retailer=retailer, is_deleted=False).count()


# ==========================================================
# VALIDATE USER SUBSCRIPTION LIMIT
# ==========================================================


def validate_user_subscription(retailer):

    subscription = check_subscription_write_access(retailer)

    max_users = subscription.plan.max_users

    if max_users == 0:
        return subscription

    current_users = get_current_user_count(retailer)

    if current_users >= max_users:

        raise ValidationError(
            {
                "subscription": (
                    f"User limit reached. "
                    f"Your current plan allows a maximum of "
                    f"{max_users} users."
                )
            }
        )

    return subscription


# ==========================================================
# GET CURRENT PRODUCT COUNT
# ==========================================================


def get_current_product_count(retailer):

    from masters.models import Product

    return Product.objects.filter(retailer=retailer).count()


# ==========================================================
# VALIDATE PRODUCT SUBSCRIPTION LIMIT
# ==========================================================


def validate_product_subscription(retailer):

    subscription = check_subscription_write_access(retailer)
    max_products = subscription.plan.max_products


    if max_products == 0:
        return subscription

    current_products = get_current_product_count(retailer)

    if current_products >= max_products:

        raise ValidationError(
            {
                "subscription": (
                    f"Product limit reached. "
                    f"Your current plan allows a maximum of "
                    f"{max_products} products."
                )
            }
        )

    return subscription
