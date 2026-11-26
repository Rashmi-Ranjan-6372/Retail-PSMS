from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from accounts.views import create_audit_log

from reports.services import (
    AnalyticsService,
    CustomerLedgerService,
    DashboardService,
    ExpiryReportService,
    GSTReportService,
    LowStockReportService,
    PaymentReportService,
    ProductLedgerService,
    ProfitLossService,
    PurchaseReportService,
    PurchaseReturnReportService,
    ReceiptReportService,
    SalesReportService,
    SalesReturnReportService,
    StockAdjustmentReportService,
    StockReportService,
    StockTransferReportService,
    SupplierLedgerService,
)

# ============================================================
# BASE REPORT VIEW
# ============================================================


class BaseReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get_report_scope(self, request):
        retailer = getattr(request.user, "retailer", None)

        if retailer is None:
            raise PermissionDenied("Your account is not associated with a retailer.")

        branch = getattr(request.user, "branch", None)

        return retailer, branch

    def get_required_param(self, request, parameter):
        value = request.query_params.get(parameter)

        if not value:
            return None

        return value

    def audit_report(self, request, model_name, object_id=None, description=""):
        create_audit_log(
            user=request.user,
            action="view",
            model_name=model_name,
            object_id=object_id,
            description=description,
            request=request,
        )


# ============================================================
# ANALYTICS REPORT
# ============================================================


class AnalyticsView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        data = AnalyticsService.get_analytics(retailer=retailer, branch=branch)

        self.audit_report(request, "Analytics", retailer.id, "Viewed Analytics Report")

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# CUSTOMER LEDGER
# ============================================================


class CustomerLedgerView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        customer_id = self.get_required_param(request, "customer")

        if not customer_id:
            return Response(
                {"success": False, "message": "Customer ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = CustomerLedgerService.get_customer_ledger(
            customer_id=customer_id, retailer=retailer, branch=branch
        )

        self.audit_report(
            request,
            "CustomerLedger",
            customer_id,
            f"Viewed Customer Ledger for Customer {customer_id}",
        )

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# DASHBOARD REPORT
# ============================================================


class DashboardView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        data = DashboardService.get_dashboard(retailer=retailer, branch=branch)

        self.audit_report(
            request,
            "Dashboard",
            branch.id if branch else retailer.id,
            "Viewed Dashboard Report",
        )

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# EXPIRY REPORT
# ============================================================


class ExpiryReportView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        data = ExpiryReportService.get_report(retailer=retailer, branch=branch)

        self.audit_report(
            request,
            "ExpiryReport",
            branch.id if branch else retailer.id,
            "Viewed Expiry Report",
        )

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# GST REPORT
# ============================================================


class GSTReportView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        data = GSTReportService.get_report(retailer=retailer, branch=branch)

        self.audit_report(request, "GSTReport", retailer.id, "Viewed GST Report")

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# LOW STOCK REPORT
# ============================================================


class LowStockReportView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        data = LowStockReportService.get_report(retailer=retailer, branch=branch)

        self.audit_report(
            request,
            "LowStockReport",
            branch.id if branch else retailer.id,
            "Viewed Low Stock Report",
        )

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# PAYMENT REPORT
# ============================================================


class PaymentReportView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        data = PaymentReportService.get_report(retailer=retailer, branch=branch)

        self.audit_report(
            request, "PaymentReport", retailer.id, "Viewed Payment Report"
        )

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# PRODUCT LEDGER
# ============================================================


class ProductLedgerView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        product_id = self.get_required_param(request, "product")

        if not product_id:
            return Response(
                {"success": False, "message": "Product ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = ProductLedgerService.get_product_ledger(
            product_id=product_id, retailer=retailer, branch=branch
        )

        self.audit_report(
            request,
            "ProductLedger",
            product_id,
            f"Viewed Product Ledger for Product {product_id}",
        )

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# PROFIT AND LOSS REPORT
# ============================================================


class ProfitLossView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        data = ProfitLossService.get_report(retailer=retailer, branch=branch)

        self.audit_report(
            request,
            "ProfitLossReport",
            branch.id if branch else retailer.id,
            "Viewed Profit and Loss Report",
        )

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# PURCHASE REPORT
# ============================================================


class PurchaseReportView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        data = PurchaseReportService.get_report(retailer=retailer, branch=branch)

        self.audit_report(
            request,
            "PurchaseReport",
            branch.id if branch else retailer.id,
            "Viewed Purchase Report",
        )

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# PURCHASE RETURN REPORT
# ============================================================


class PurchaseReturnReportView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        data = PurchaseReturnReportService.get_report(retailer=retailer, branch=branch)

        self.audit_report(
            request,
            "PurchaseReturnReport",
            branch.id if branch else retailer.id,
            "Viewed Purchase Return Report",
        )

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# RECEIPT REPORT
# ============================================================


class ReceiptReportView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        data = ReceiptReportService.get_report(retailer=retailer, branch=branch)

        self.audit_report(
            request, "ReceiptReport", retailer.id, "Viewed Receipt Report"
        )

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# SALES REPORT
# ============================================================


class SalesReportView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        filters = {
            key: value
            for key, value in request.query_params.items()
            if key not in ("retailer", "branch")
        }

        data = SalesReportService.get_sales_report(
            filters=filters, retailer=retailer, branch=branch
        )

        self.audit_report(
            request,
            "SalesReport",
            branch.id if branch else retailer.id,
            "Viewed Sales Report",
        )

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# SALES RETURN REPORT
# ============================================================


class SalesReturnReportView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        data = SalesReturnReportService.get_report(retailer=retailer, branch=branch)

        self.audit_report(
            request,
            "SalesReturnReport",
            branch.id if branch else retailer.id,
            "Viewed Sales Return Report",
        )

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# STOCK ADJUSTMENT REPORT
# ============================================================


class StockAdjustmentReportView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        data = StockAdjustmentReportService.get_report(retailer=retailer, branch=branch)

        self.audit_report(
            request,
            "StockAdjustmentReport",
            retailer.id,
            "Viewed Stock Adjustment Report",
        )

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# STOCK REPORT
# ============================================================


class StockReportView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        data = StockReportService.get_report(retailer=retailer, branch=branch)

        self.audit_report(
            request,
            "StockReport",
            branch.id if branch else retailer.id,
            "Viewed Stock Report",
        )

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# STOCK TRANSFER REPORT
# ============================================================


class StockTransferReportView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        data = StockTransferReportService.get_report(retailer=retailer, branch=branch)

        self.audit_report(
            request, "StockTransferReport", retailer.id, "Viewed Stock Transfer Report"
        )

        return Response(data, status=status.HTTP_200_OK)


# ============================================================
# SUPPLIER LEDGER
# ============================================================


class SupplierLedgerView(BaseReportView):

    def get(self, request):
        retailer, branch = self.get_report_scope(request)

        supplier_id = self.get_required_param(request, "supplier")

        if not supplier_id:
            return Response(
                {"success": False, "message": "Supplier ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = SupplierLedgerService.get_supplier_ledger(
            supplier_id=supplier_id, retailer=retailer, branch=branch
        )

        self.audit_report(
            request,
            "SupplierLedger",
            supplier_id,
            f"Viewed Supplier Ledger for Supplier {supplier_id}",
        )

        return Response(data, status=status.HTTP_200_OK)
