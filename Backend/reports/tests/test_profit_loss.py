from django.test import TestCase
from reports.services.profit_loss_service import ProfitLossService


class ProfitLossReportTest(TestCase):

    def test_profit_loss_report(self):

        response = ProfitLossService.get_report()

        self.assertIn("sales", response)
        self.assertIn("purchase", response)
        self.assertIn("profit", response)