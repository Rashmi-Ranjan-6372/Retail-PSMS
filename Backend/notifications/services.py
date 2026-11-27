from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from notifications.models import Notification

User = get_user_model()


# =====================================================
# PLATFORM OWNER VALIDATION
# =====================================================


def is_platform_owner(user):

    return (
        user is not None
        and user.is_authenticated
        and user.is_active
        and (user.is_superuser or getattr(user, "role", None) == "platform_owner")
    )


# =====================================================
# RECIPIENT VALIDATION
# =====================================================


def validate_platform_recipient(user):

    if not is_platform_owner(user):
        raise ValidationError("Notification recipient must be a Platform Owner.")


def validate_retailer_recipient(user, retailer):

    if not user or not user.is_authenticated or not user.is_active:
        raise ValidationError("Invalid or inactive notification recipient.")

    if is_platform_owner(user):
        raise ValidationError(
            "Platform Owner cannot receive retailer-scoped notifications."
        )

    if not user.retailer_id or user.retailer_id != retailer.id:
        raise ValidationError("Recipient does not belong to this retailer.")


def validate_branch(branch, retailer):

    if branch is None:
        return

    if (
        branch.retailer_id != retailer.id
        or not branch.is_active
        or branch.deleted_at is not None
    ):
        raise ValidationError(
            "Branch must be active and belong to the selected retailer."
        )


# =====================================================
# CREATE PLATFORM OWNER NOTIFICATION
# =====================================================


@transaction.atomic
def create_platform_notification(
    title,
    message,
    notification_type="general",
    priority="normal",
    recipient=None,
):

    if recipient is not None:
        recipients = [recipient]
    else:
        recipients = User.objects.filter(
            Q(is_superuser=True) | Q(role="platform_owner"),
            is_active=True,
        ).distinct()

    notifications = []

    for user in recipients:

        validate_platform_recipient(user)

        notification = Notification.objects.create(
            scope="platform",
            retailer=None,
            branch=None,
            recipient=user,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
        )

        notifications.append(notification)

    return notifications


# =====================================================
# CREATE RETAILER NOTIFICATION
# =====================================================


@transaction.atomic
def create_retailer_notification(
    retailer,
    title,
    message,
    recipients,
    notification_type="general",
    priority="normal",
    branch=None,
):

    validate_branch(branch, retailer)

    notifications = []

    for user in recipients:

        validate_retailer_recipient(user, retailer)

        notification = Notification.objects.create(
            scope="retailer",
            retailer=retailer,
            branch=branch,
            recipient=user,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
        )

        notifications.append(notification)

    return notifications


# =====================================================
# CREATE NOTIFICATION FOR ALL RETAILER USERS
# =====================================================


@transaction.atomic
def create_notification_for_all_retailer_users(
    retailer,
    title,
    message,
    notification_type="general",
    priority="normal",
    branch=None,
):

    validate_branch(branch, retailer)

    users = User.objects.filter(
        retailer_id=retailer.id,
        is_active=True,
    )

    if branch is not None:
        users = users.filter(branch_id=branch.id)

    return create_retailer_notification(
        retailer=retailer,
        title=title,
        message=message,
        recipients=users,
        notification_type=notification_type,
        priority=priority,
        branch=branch,
    )


# =====================================================
# MARK SINGLE NOTIFICATION AS READ
# =====================================================


@transaction.atomic
def mark_notification_as_read(notification_id, user):

    notification = Notification.objects.filter(
        id=notification_id,
        recipient=user,
    ).first()

    if notification is None:
        raise ValidationError("Notification not found.")

    if not notification.is_read:
        notification.is_read = True
        notification.read_at = timezone.now()

        notification.save(
            update_fields=[
                "is_read",
                "read_at",
                "updated_at",
            ]
        )

    return notification


# =====================================================
# MARK ALL NOTIFICATIONS AS READ
# =====================================================


@transaction.atomic
def mark_all_notifications_as_read(user):

    return Notification.objects.filter(
        recipient=user,
        is_read=False,
    ).update(
        is_read=True,
        read_at=timezone.now(),
    )


# =====================================================
# DELETE SINGLE NOTIFICATION
# =====================================================


def delete_notification(notification_id, user):

    notification = Notification.objects.filter(
        id=notification_id,
        recipient=user,
    ).first()

    if notification is None:
        raise ValidationError("Notification not found.")

    notification.delete()

    return True


# =====================================================
# GET UNREAD NOTIFICATION COUNT
# =====================================================


def get_unread_notification_count(user):

    return Notification.objects.filter(
        recipient=user,
        is_read=False,
    ).count()


# =====================================================
# GET USER NOTIFICATIONS
# =====================================================


def get_user_notifications(user):

    return (
        Notification.objects.filter(
            recipient=user,
        )
        .select_related(
            "retailer",
            "branch",
            "recipient",
        )
        .order_by("-created_at")
    )
