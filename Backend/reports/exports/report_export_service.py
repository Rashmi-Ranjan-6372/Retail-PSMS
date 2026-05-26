from .excel_export import ExcelExport
from .pdf_export import PDFExport
from .csv_export import CSVExport


class ReportExportService:

    @staticmethod
    def export_report(
        data,
        export_type="excel",
        file_name="report"
    ):

        if export_type == "excel":

            return ExcelExport.export(
                data=data,
                file_name=f"{file_name}.xlsx"
            )

        elif export_type == "pdf":

            return PDFExport.export(
                data=data,
                file_name=f"{file_name}.pdf"
            )

        elif export_type == "csv":

            return CSVExport.export(
                data=data,
                file_name=f"{file_name}.csv"
            )

        raise ValueError(
            "Invalid export type"
        )