import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from settings.models.models import GeneralSetting, FinancialYear

logger = logging.getLogger(__name__)


# ==========================================
# GENERAL SETTINGS SIGNAL
# ==========================================


@receiver(post_save, sender=GeneralSetting, dispatch_uid="general_setting_post_save")
def general_setting_post_save(sender, instance, created, **kwargs):

    if created:
        logger.info(
            "General settings created for retailer: %s (ID: %s)",
            instance.retailer,
            instance.retailer_id,
        )

    else:
        logger.info(
            "General settings updated for retailer: %s (ID: %s)",
            instance.retailer,
            instance.retailer_id,
        )


# ==========================================
# FINANCIAL YEAR SIGNAL
# ==========================================


@receiver(post_save, sender=FinancialYear, dispatch_uid="financial_year_post_save")
def financial_year_post_save(sender, instance, created, **kwargs):

    scope = f"Branch: {instance.branch}" if instance.branch_id else "All Branches"

    if created:
        logger.info(
            "Financial year created: %s | Retailer: %s | Scope: %s",
            instance.name,
            instance.retailer_id,
            scope,
        )

    else:
        logger.info(
            "Financial year updated: %s | Retailer: %s | Scope: %s",
            instance.name,
            instance.retailer_id,
            scope,
        )

    if instance.is_active:
        logger.info(
            "Active financial year: %s | Retailer: %s | Scope: %s",
            instance.name,
            instance.retailer_id,
            scope,
        )
