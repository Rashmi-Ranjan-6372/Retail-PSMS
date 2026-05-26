from django.test import TestCase
from reports.services.purchase_report_service import PurchaseReportService


class PurchaseReportTest(TestCase):

    def test_purchase_report(self):

        response = PurchaseReportService.get_report()

        self.assertIsInstance(response, list)