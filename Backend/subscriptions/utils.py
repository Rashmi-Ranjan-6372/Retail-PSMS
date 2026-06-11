from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import RetailerSubscription
from branches.models import Branch
from accounts.models import User
from rest_framework.exceptions import PermissionDenied

def get_subscription(retailer):

    return (
        RetailerSubscription.objects
        .filter(retailer=retailer)
        .select_related("plan")
        .first()
    )


def is_subscription_active(retailer):

    subscription = get_subscription(retailer)

    if not subscription:
        return False

    if subscription.status != "active":
        return False

    if subscription.expiry_date < timezone.now().date():
        return False

    return True


def check_subscription_write_access(retailer):

    subscription = get_subscription(retailer)

    if not subscription:
        raise PermissionDenied(
            "No subscription assigned."
        )

    if subscription.status != "active":
        raise PermissionDenied(
            "Subscription is suspended."
        )

    if subscription.expiry_date < timezone.now().date():
        raise PermissionDenied(
            "Subscription expired. Please renew your subscription."
        )

    return subscription


def validate_branch_subscription(retailer):

    subscription = check_subscription_write_access(retailer)

    if subscription.plan.max_branches > 0:

        current_branches = Branch.objects.filter(
            retailer=retailer,
            deleted_at__isnull=True
        ).count()

        if current_branches >= subscription.plan.max_branches:

            raise ValidationError(
                f"Branch limit reached. Allowed: "
                f"{subscription.plan.max_branches}"
            )

    return subscription


def validate_user_subscription(retailer):

    subscription = check_subscription_write_access(retailer)

    if subscription.plan.max_users > 0:

        current_users = User.objects.filter(
            retailer=retailer,
            is_deleted=False
        ).count()

        if current_users >= subscription.plan.max_users:

            raise ValidationError(
                f"User limit reached. Allowed: "
                f"{subscription.plan.max_users}"
            )

    return subscription