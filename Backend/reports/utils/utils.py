
import csv

import pandas as pd

from datetime import timedelta
from decimal import Decimal

from django.db.models import Sum, Count, DecimalField
from django.db.models.functions import Coalesce
from django.utils.timezone import now

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


MONEY_FIELD = DecimalField(max_digits=15, decimal_places=2)


# ============================================================
# CHART HELPERS
# ============================================================

def generate_chart_data(labels, values):
    return {
        "labels": labels,
        "datasets": [
            {
                "data": values
            }
        ]
    }


# ============================================================
# CSV EXPORT
# ============================================================

def generate_csv(data, headers, file_name="report.csv"):
    with open(file_name, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        writer.writerow(headers)

        for row in data:
            writer.writerow(row)

    return file_name


# ============================================================
# EXCEL EXPORT
# ============================================================

def generate_excel(data, file_name="report.xlsx"):
    dataframe = pd.DataFrame(data)

    dataframe.to_excel(
        file_name,
        index=False
    )

    return file_name


# ============================================================
# PDF EXPORT
# ============================================================

def generate_pdf(data, file_name="report.pdf"):
    document = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    elements = []

    for item in data:
        elements.append(
            Paragraph(str(item), styles["BodyText"])
        )

    document.build(elements)

    return file_name


# ============================================================
# DASHBOARD HELPERS
# ============================================================

def get_dashboard_summary(queryset, field):
    return queryset.values(field).annotate(
        total=Count(field)
    )


def prepare_dashboard_card(title, value):
    return {
        "title": title,
        "value": value
    }


# ============================================================
# DATE RANGE HELPERS
# ============================================================

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


# ============================================================
# SALES AND PURCHASE CALCULATIONS
# ============================================================

def calculate_sales_total(queryset):
    return queryset.aggregate(
        total=Coalesce(
            Sum("net_amount"),
            Decimal("0.00"),
            output_field=MONEY_FIELD
        )
    )["total"]


def calculate_purchase_total(queryset):
    return queryset.aggregate(
        total=Coalesce(
            Sum("total_amount"),
            Decimal("0.00"),
            output_field=MONEY_FIELD
        )
    )["total"]


def calculate_profit(sales, purchase):
    return sales - purchase


# ============================================================
# SUPPLIER AND CUSTOMER BALANCE
# ============================================================

def calculate_supplier_balance(queryset):
    return queryset.aggregate(
        total=Coalesce(
            Sum("due_amount"),
            Decimal("0.00"),
            output_field=MONEY_FIELD
        )
    )["total"]


def calculate_customer_balance(queryset):
    return queryset.aggregate(
        total=Coalesce(
            Sum("due_amount"),
            Decimal("0.00"),
            output_field=MONEY_FIELD
        )
    )["total"]


# ============================================================
# GENERAL REPORT CALCULATIONS
# ============================================================

def calculate_total(queryset, field):
    return queryset.aggregate(
        total=Coalesce(
            Sum(field),
            Decimal("0.00"),
            output_field=MONEY_FIELD
        )
    )["total"]


def format_currency(amount):
    return round(float(amount or 0), 2)


def get_percentage(value, total):
    if total == 0:
        return 0

    return round((value / total) * 100, 2)


# ============================================================
# STOCK HELPERS
# ============================================================

def total_stock(queryset):
    return queryset.aggregate(
        total=Coalesce(
            Sum("available_qty"),
            Decimal("0.000")
        )
    )["total"]


def low_stock(queryset, limit=10):
    return queryset.filter(
        available_qty__lte=limit,
        available_qty__gt=0
    )


def expired_stock(queryset):
    return queryset.filter(
        is_expired=True
    )
