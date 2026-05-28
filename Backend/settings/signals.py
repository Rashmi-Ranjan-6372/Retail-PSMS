# settings/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver

from settings.models.general_setting_models import (
    GeneralSetting
)

from settings.models.financial_year_models import (
    FinancialYear
)


# =========================
# GENERAL SETTINGS SIGNAL
# =========================

@receiver(post_save, sender=GeneralSetting)
def general_setting_post_save(
    sender,
    instance,
    created,
    **kwargs
):

    if created:

        print(
            f"General settings created for retailer: "
            f"{instance.retailer}"
        )

    else:

        print(
            f"General settings updated for retailer: "
            f"{instance.retailer}"
        )


# =========================
# FINANCIAL YEAR SIGNAL
# =========================

@receiver(post_save, sender=FinancialYear)
def financial_year_post_save(
    sender,
    instance,
    created,
    **kwargs
):

    if created:

        print(
            f"Financial year created: "
            f"{instance.financial_year_name}"
        )

    else:

        print(
            f"Financial year updated: "
            f"{instance.financial_year_name}"
        )

    # =========================
    # AUTO CLOSE OTHER YEARS
    # =========================

    if instance.is_active:

        FinancialYear.objects.filter(
            retailer=instance.retailer
        ).exclude(
            id=instance.id
        ).update(
            is_active=False
        )