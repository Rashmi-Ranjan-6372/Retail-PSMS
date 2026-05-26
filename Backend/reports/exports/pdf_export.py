from django.http import HttpResponse
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle
)
from reportlab.lib import colors


class PDFExport:

    @staticmethod
    def export(data, file_name="report.pdf"):

        response = HttpResponse(
            content_type="application/pdf"
        )

        response[
            "Content-Disposition"
        ] = f'attachment; filename="{file_name}"'

        document = SimpleDocTemplate(response)

        elements = []

        if data:

            headers = list(data[0].keys())

            table_data = [headers]

            for row in data:

                table_data.append(
                    list(row.values())
                )

            table = Table(table_data)

            table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ])
            )

            elements.append(table)

        document.build(elements)

        return response