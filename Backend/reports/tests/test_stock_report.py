from django.test import TestCase
from reports.services.stock_report_service import StockReportService


class StockReportTest(TestCase):

    def test_stock_report(self):

        response = StockReportService.get_report()

        self.assertIsInstance(response, list)