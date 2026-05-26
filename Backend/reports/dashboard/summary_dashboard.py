from dashboard.sales_dashboard import SalesDashboardService
from dashboard.stock_dashboard import StockDashboardService
from dashboard.finance_dashboard import FinanceDashboardService


class SummaryDashboardService:

    @staticmethod
    def get_dashboard(retailer=None, branch=None):

        sales_data = (
            SalesDashboardService.get_dashboard(
                retailer=retailer,
                branch=branch
            )
        )

        stock_data = (
            StockDashboardService.get_dashboard(
                retailer=retailer,
                branch=branch
            )
        )

        finance_data = (
            FinanceDashboardService.get_dashboard(
                retailer=retailer,
                branch=branch
            )
        )

        return {
            "sales": sales_data,
            "stock": stock_data,
            "finance": finance_data,
        }