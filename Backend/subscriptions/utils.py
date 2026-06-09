from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import RetailerSubscription
from branches.models import Branch
from accounts.models import User


def get_active_subscription(retailer):

    subscription = (
        RetailerSubscription.objects
        .filter(
            retailer=retailer,
            is_active=True,
            end_date__gte=timezone.now().date()
        )
        .select_related("plan")
        .first()
    )

    if not subscription:
        raise ValidationError(
            "No active subscription found."
        )

    return subscription


def validate_branch_subscription(retailer):

    subscription = get_active_subscription(retailer)

    if subscription.plan.max_branches > 0:

        current_branches = Branch.objects.filter(
            retailer=retailer,
            deleted_at__isnull=True
        ).count()

        if current_branches >= subscription.plan.max_branches:

            raise ValidationError(
                f"Branch limit reached. "
                f"Allowed: {subscription.plan.max_branches}"
            )

    return subscription


def validate_user_subscription(retailer):

    subscription = get_active_subscription(retailer)

    if subscription.plan.max_users > 0:

        current_users = User.objects.filter(
            retailer=retailer,
            is_deleted=False
        ).count()

        if current_users >= subscription.plan.max_users:

            raise ValidationError(
                f"User limit reached. "
                f"Allowed: {subscription.plan.max_users}"
            )

    return subscription