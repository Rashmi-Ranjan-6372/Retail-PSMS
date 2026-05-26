import csv
from django.http import HttpResponse


class CSVExport:

    @staticmethod
    def export(data, file_name="report.csv"):

        response = HttpResponse(
            content_type="text/csv"
        )

        response[
            "Content-Disposition"
        ] = f'attachment; filename="{file_name}"'

        writer = csv.writer(response)

        if data:

            headers = data[0].keys()

            writer.writerow(headers)

            for row in data:

                writer.writerow(
                    row.values()
                )

        return response