from datetime import timedelta
from django.utils.timezone import now


def today_range():

    today = now().date()

    return today, today


def weekly_range():

    end_date = now().date()
    start_date = end_date - timedelta(days=7)

    return start_date, end_date


def monthly_range():

    end_date = now().date()
    start_date = end_date.replace(day=1)

    return start_date, end_date