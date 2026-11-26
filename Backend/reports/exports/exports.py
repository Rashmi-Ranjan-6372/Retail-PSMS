import csv
from io import BytesIO

import pandas as pd

from django.http import HttpResponse

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm

# =========================
# EXPORT CONFIGURATION
# =========================

EXPORT_CONTENT_TYPES = {
    "CSV": "text/csv",
    "EXCEL": ("application/vnd.openxmlformats-officedocument." "spreadsheetml.sheet"),
    "PDF": "application/pdf",
}


# =========================
# COMMON EXPORT HELPERS
# =========================


def normalize_export_data(data):
    """
    Convert queryset or iterable of dictionaries into a list.
    """

    if data is None:
        return []

    if hasattr(data, "values") and callable(data.values):
        return list(data.values())

    return list(data)


def get_export_headers(data, headers=None):
    """
    Get consistent column headers.
    """

    if headers:
        return list(headers)

    if data:
        return list(data[0].keys())

    return []


def prepare_export_rows(data, headers):
    """
    Prepare rows using header order instead of dictionary value order.
    """

    rows = []

    for item in data:
        if isinstance(item, dict):
            rows.append([item.get(header, "") for header in headers])
        else:
            rows.append(list(item))

    return rows


# =========================
# CSV EXPORT
# =========================


class CSVExport:

    @staticmethod
    def export(data, file_name="report.csv", headers=None):

        data = normalize_export_data(data)

        export_headers = get_export_headers(
            data,
            headers=headers,
        )

        response = HttpResponse(
            content_type=EXPORT_CONTENT_TYPES["CSV"],
        )

        response["Content-Disposition"] = f'attachment; filename="{file_name}"'

        response.write("\ufeff")

        writer = csv.writer(response)

        if export_headers:
            writer.writerow(export_headers)

            rows = prepare_export_rows(
                data,
                export_headers,
            )

            writer.writerows(rows)

        return response


# =========================
# EXCEL EXPORT
# =========================


class ExcelExport:

    @staticmethod
    def export(data, file_name="report.xlsx", headers=None):

        data = normalize_export_data(data)

        export_headers = get_export_headers(
            data,
            headers=headers,
        )

        rows = prepare_export_rows(
            data,
            export_headers,
        )

        dataframe = pd.DataFrame(
            rows,
            columns=export_headers,
        )

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl",
        ) as writer:

            dataframe.to_excel(
                writer,
                index=False,
                sheet_name="Report",
            )

            worksheet = writer.sheets["Report"]

            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions

            for column_cells in worksheet.columns:

                max_length = max(len(str(cell.value or "")) for cell in column_cells)

                column_letter = column_cells[0].column_letter

                worksheet.column_dimensions[column_letter].width = min(
                    max_length + 2, 40
                )

        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type=EXPORT_CONTENT_TYPES["EXCEL"],
        )

        response["Content-Disposition"] = f'attachment; filename="{file_name}"'

        return response


# =========================
# PDF EXPORT
# =========================


class PDFExport:

    @staticmethod
    def export(data, file_name="report.pdf", headers=None):

        data = normalize_export_data(data)

        export_headers = get_export_headers(
            data,
            headers=headers,
        )

        rows = prepare_export_rows(
            data,
            export_headers,
        )

        response = HttpResponse(
            content_type=EXPORT_CONTENT_TYPES["PDF"],
        )

        response["Content-Disposition"] = f'attachment; filename="{file_name}"'

        document = SimpleDocTemplate(
            response,
            pagesize=landscape(A4),
            rightMargin=10 * mm,
            leftMargin=10 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm,
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=16,
            spaceAfter=12,
        )

        cell_style = ParagraphStyle(
            "TableCell",
            parent=styles["Normal"],
            fontSize=7,
            leading=9,
        )

        elements = []

        elements.append(Paragraph("Report", title_style))

        elements.append(Spacer(1, 5 * mm))

        if export_headers:

            table_data = [
                [
                    Paragraph(
                        str(header),
                        cell_style,
                    )
                    for header in export_headers
                ]
            ]

            for row in rows:

                table_data.append(
                    [
                        Paragraph(
                            str(value if value is not None else ""),
                            cell_style,
                        )
                        for value in row
                    ]
                )

            table = Table(
                table_data,
                repeatRows=1,
                hAlign="LEFT",
            )

            table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            colors.HexColor("#343A40"),
                        ),
                        (
                            "TEXTCOLOR",
                            (0, 0),
                            (-1, 0),
                            colors.whitesmoke,
                        ),
                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, 0),
                            "Helvetica-Bold",
                        ),
                        (
                            "ALIGN",
                            (0, 0),
                            (-1, -1),
                            "LEFT",
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "MIDDLE",
                        ),
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.5,
                            colors.grey,
                        ),
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -1),
                            [
                                colors.white,
                                colors.HexColor("#F2F2F2"),
                            ],
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            5,
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            5,
                        ),
                    ]
                )
            )

            elements.append(table)

        else:

            elements.append(Paragraph("No data available.", styles["Normal"]))

        document.build(elements)

        return response


# =========================
# REPORT EXPORT SERVICE
# =========================


class ReportExportService:

    @staticmethod
    def export_report(
        data,
        export_type="EXCEL",
        file_name="report",
        headers=None,
    ):

        export_type = str(export_type).strip().upper()

        file_name = str(file_name).strip()

        if not file_name:
            file_name = "report"

        # Remove an existing supported extension.
        for extension in (".xlsx", ".csv", ".pdf"):
            if file_name.lower().endswith(extension):
                file_name = file_name[: -len(extension)]
                break

        if export_type == "EXCEL":

            return ExcelExport.export(
                data=data,
                file_name=f"{file_name}.xlsx",
                headers=headers,
            )

        elif export_type == "PDF":

            return PDFExport.export(
                data=data,
                file_name=f"{file_name}.pdf",
                headers=headers,
            )

        elif export_type == "CSV":

            return CSVExport.export(
                data=data,
                file_name=f"{file_name}.csv",
                headers=headers,
            )

        raise ValueError("Invalid export type. Allowed types: PDF, EXCEL, CSV.")
