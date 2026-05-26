import pandas as pd
from django.http import HttpResponse


class ExcelExport:

    @staticmethod
    def export(data, file_name="report.xlsx"):

        df = pd.DataFrame(data)

        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        )

        response[
            "Content-Disposition"
        ] = f'attachment; filename="{file_name}"'

        with pd.ExcelWriter(
            response,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False
            )

        return response