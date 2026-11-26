from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import Retailer
from branches.models import Branch

from inventory.models.sales_models import Sales
from inventory.models.stock_transaction_models import StockTransaction

from reports.services import (
    DashboardService,
    ProfitLossService,
    PurchaseReportService,
    SalesReportService,
    StockReportService,
    apply_report_scope,
)


class ReportTestBase(TestCase):

    def setUp(self):

        self.retailer = Retailer.objects.create(
            name="Test Pharmacy",
            owner_name="Test Owner",
            mobile="9876543210",
            email="testpharmacy@example.com",
        )

        self.other_retailer = Retailer.objects.create(
            name="Other Pharmacy",
            owner_name="Other Owner",
            mobile="9876543211",
            email="otherpharmacy@example.com",
        )

        self.branch = Branch.objects.create(
            retailer=self.retailer,
            name="Main Branch",
            address="Cuttack",
            phone="9876543212",
        )

        self.other_branch = Branch.objects.create(
            retailer=self.other_retailer,
            name="Other Branch",
            address="Bhubaneswar",
            phone="9876543213",
        )

    def create_sale(
        self,
        retailer,
        branch,
        invoice_amount,
        paid_amount=Decimal("0.00"),
    ):

        return Sales.objects.create(
            retailer=retailer,
            branch=branch,
            total_amount=invoice_amount,
            discount=Decimal("0.00"),
            paid_amount=paid_amount,
        )

    def create_purchase(
        self,
        retailer,
        branch,
        amount,
    ):

        return StockTransaction.objects.create(
            retailer=retailer,
            branch=branch,
            transaction_type="PURCHASE",
            total_amount=amount,
        )


class ReportScopeTest(ReportTestBase):

    def test_retailer_scope(self):

        self.create_sale(
            self.retailer,
            self.branch,
            Decimal("1000.00"),
        )

        self.create_sale(
            self.other_retailer,
            self.other_branch,
            Decimal("2000.00"),
        )

        queryset = apply_report_scope(
            Sales.objects.all(),
            retailer=self.retailer,
        )

        self.assertEqual(queryset.count(), 1)

    def test_branch_scope(self):

        self.create_sale(
            self.retailer,
            self.branch,
            Decimal("1000.00"),
        )

        queryset = apply_report_scope(
            Sales.objects.all(),
            branch=self.branch,
        )

        self.assertEqual(queryset.count(), 1)

    def test_scope_required(self):

        with self.assertRaises(ValidationError):

            apply_report_scope(
                Sales.objects.all(),
            )


class DashboardReportTest(ReportTestBase):

    def test_dashboard_summary(self):

        self.create_sale(
            self.retailer,
            self.branch,
            Decimal("1000.00"),
            Decimal("500.00"),
        )

        response = DashboardService.get_dashboard(
            retailer=self.retailer,
        )

        self.assertEqual(
            response["total_sales"],
            Decimal("1000.00"),
        )

        self.assertEqual(
            response["invoice_count"],
            1,
        )

        self.assertEqual(
            response["total_stock"],
            Decimal("0.00"),
        )

    def test_dashboard_retailer_isolation(self):

        self.create_sale(
            self.retailer,
            self.branch,
            Decimal("1000.00"),
        )

        self.create_sale(
            self.other_retailer,
            self.other_branch,
            Decimal("2000.00"),
        )

        response = DashboardService.get_dashboard(
            retailer=self.retailer,
        )

        self.assertEqual(
            response["total_sales"],
            Decimal("1000.00"),
        )

        self.assertEqual(
            response["invoice_count"],
            1,
        )


class SalesReportTest(ReportTestBase):

    def test_sales_report_summary(self):

        self.create_sale(
            self.retailer,
            self.branch,
            Decimal("1000.00"),
            Decimal("600.00"),
        )

        response = SalesReportService.get_sales_report(
            retailer=self.retailer,
        )

        summary = response["summary"]

        self.assertEqual(
            summary["total_sales"],
            Decimal("1000.00"),
        )

        self.assertEqual(
            summary["total_paid"],
            Decimal("600.00"),
        )

        self.assertEqual(
            summary["total_due"],
            Decimal("400.00"),
        )

        self.assertEqual(
            summary["invoice_count"],
            1,
        )

    def test_sales_report_retailer_isolation(self):

        self.create_sale(
            self.retailer,
            self.branch,
            Decimal("1000.00"),
        )

        self.create_sale(
            self.other_retailer,
            self.other_branch,
            Decimal("2000.00"),
        )

        response = SalesReportService.get_sales_report(
            retailer=self.retailer,
        )

        self.assertEqual(
            response["summary"]["invoice_count"],
            1,
        )

    def test_sales_report_branch_filter(self):

        self.create_sale(
            self.retailer,
            self.branch,
            Decimal("1000.00"),
        )

        response = SalesReportService.get_sales_report(
            branch=self.branch,
        )

        self.assertEqual(
            response["summary"]["total_sales"],
            Decimal("1000.00"),
        )


class PurchaseReportTest(ReportTestBase):

    def test_purchase_report_summary(self):

        self.create_purchase(
            self.retailer,
            self.branch,
            Decimal("5000.00"),
        )

        response = PurchaseReportService.get_report(
            retailer=self.retailer,
        )

        self.assertEqual(
            response["summary"]["total_purchase"],
            Decimal("5000.00"),
        )

        self.assertEqual(
            response["summary"]["purchase_count"],
            1,
        )

    def test_purchase_report_retailer_isolation(self):

        self.create_purchase(
            self.retailer,
            self.branch,
            Decimal("5000.00"),
        )

        self.create_purchase(
            self.other_retailer,
            self.other_branch,
            Decimal("8000.00"),
        )

        response = PurchaseReportService.get_report(
            retailer=self.retailer,
        )

        self.assertEqual(
            response["summary"]["total_purchase"],
            Decimal("5000.00"),
        )

        self.assertEqual(
            response["summary"]["purchase_count"],
            1,
        )


class ProfitLossReportTest(ReportTestBase):

    def test_profit_loss_report(self):

        self.create_sale(
            self.retailer,
            self.branch,
            Decimal("10000.00"),
        )

        self.create_purchase(
            self.retailer,
            self.branch,
            Decimal("6000.00"),
        )

        response = ProfitLossService.get_report(
            retailer=self.retailer,
        )

        self.assertEqual(
            response["overall"]["sales"],
            Decimal("10000.00"),
        )

        self.assertEqual(
            response["overall"]["purchase"],
            Decimal("6000.00"),
        )

        self.assertIsNone(
            response["overall"]["profit"],
        )

        self.assertIsInstance(
            response["branch_wise"],
            list,
        )

        self.assertIn(
            "COGS",
            response["message"],
        )


class StockReportTest(ReportTestBase):

    def test_stock_report_empty_summary(self):

        response = StockReportService.get_report(
            retailer=self.retailer,
        )

        self.assertEqual(
            response["summary"]["total_stock"],
            Decimal("0.00"),
        )

        self.assertEqual(
            response["summary"]["batch_count"],
            0,
        )

        self.assertEqual(
            response["data"].count(),
            0,
        )
