from django.test import TestCase
from reports.dashboard.summary_dashboard import SummaryDashboard


class DashboardTest(TestCase):

    def test_dashboard_summary(self):

        response = SummaryDashboard.get_summary()

        self.assertIsInstance(response, dict)