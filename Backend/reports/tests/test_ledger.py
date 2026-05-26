from django.test import TestCase
from reports.services.product_ledger_service import ProductLedgerService


class LedgerReportTest(TestCase):

    def test_product_ledger(self):

        response = ProductLedgerService.get_report()

        self.assertIsInstance(response, list)