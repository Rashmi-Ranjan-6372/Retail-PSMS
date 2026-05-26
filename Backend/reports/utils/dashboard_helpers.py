from django.db.models import Count


def get_dashboard_summary(queryset, field):

    return queryset.values(field).annotate(
        total=Count(field)
    )


def prepare_dashboard_card(title, value):

    return {
        "title": title,
        "value": value
    }