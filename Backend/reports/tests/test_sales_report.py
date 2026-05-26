from django.test import TestCase
from reports.services.sales_report_service import SalesReportService


class SalesReportTest(TestCase):

    def test_sales_report(self):

        response = SalesReportService.get_report()

        self.assertIsInstance(response, list)