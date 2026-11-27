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

from reports.serializers import (
    AnalyticsSerializer,
    CustomerLedgerSerializer,
    DashboardSerializer,
    ExpiryReportSerializer,
    LowStockReportSerializer,
    ProductLedgerSerializer,
    ProfitLossSerializer,
    PurchaseReportSerializer,
    PurchaseReturnReportSerializer,
    SalesReportSerializer,
    SalesReturnReportSerializer,
    StockReportSerializer,
    SupplierLedgerSerializer,
)

# ============================================================
# BASE REPORT VIEW
# ============================================================


class BaseReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get_report_scope(self, request):

        user = request.user

        if not user.is_authenticated or not user.is_active:
            raise PermissionDenied("Your account is not authorized to access reports.")

        retailer = getattr(user, "retailer", None)

        if retailer is None:
            raise PermissionDenied("Your account is not associated with a retailer.")

        if getattr(user, "role", None) == "platform_owner" or user.is_superuser:
            raise PermissionDenied(
                "Platform Owner must select a retailer before accessing retailer reports."
            )

        branch = getattr(user, "branch", None)

        if getattr(user, "role", None) == "superadmin":
            return retailer, None

        if branch is None:
            raise PermissionDenied("Your account is not assigned to a branch.")

        if (
            branch.retailer_id != retailer.id
            or not branch.is_active
            or branch.deleted_at is not None
        ):
            raise PermissionDenied("Your assigned branch is invalid or inactive.")

        return retailer, branch

    def get_required_param(self, request, parameter):

        value = request.query_params.get(parameter)

        if not value:
            return None

        return value

    def serialize_report(self, data, serializer_class=None):

        if serializer_class is None:
            return data

        is_many = isinstance(data, (list, tuple))

        serializer = serializer_class(
            data,
            many=is_many,
        )

        return serializer.data

    def report_response(
        self,
        data,
        message="Report retrieved successfully.",
        serializer_class=None,
    ):

        serialized_data = self.serialize_report(
            data=data,
            serializer_class=serializer_class,
        )

        return Response(
            {
                "success": True,
                "message": message,
                "data": serialized_data,
            },
            status=status.HTTP_200_OK,
        )

    def audit_report(
        self,
        request,
        model_name,
        object_id=None,
        description="",
    ):

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

        data = AnalyticsService.get_analytics(
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "Analytics",
            retailer.id,
            "Viewed Analytics Report",
        )

        return self.report_response(
            data=data,
            message="Analytics report retrieved successfully.",
            serializer_class=AnalyticsSerializer,
        )


# ============================================================
# CUSTOMER LEDGER
# ============================================================


class CustomerLedgerView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        customer_id = self.get_required_param(
            request,
            "customer",
        )

        if not customer_id:
            return Response(
                {
                    "success": False,
                    "message": "Customer ID is required.",
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = CustomerLedgerService.get_customer_ledger(
            customer_id=customer_id,
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "CustomerLedger",
            customer_id,
            f"Viewed Customer Ledger for Customer {customer_id}",
        )

        return self.report_response(
            data=data,
            message="Customer ledger retrieved successfully.",
            serializer_class=CustomerLedgerSerializer,
        )


# ============================================================
# DASHBOARD REPORT
# ============================================================


class DashboardView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        data = DashboardService.get_dashboard(
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "Dashboard",
            branch.id if branch else retailer.id,
            "Viewed Dashboard Report",
        )

        return self.report_response(
            data=data,
            message="Dashboard data retrieved successfully.",
            serializer_class=DashboardSerializer,
        )


# ============================================================
# EXPIRY REPORT
# ============================================================


class ExpiryReportView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        data = ExpiryReportService.get_report(
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "ExpiryReport",
            branch.id if branch else retailer.id,
            "Viewed Expiry Report",
        )

        return self.report_response(
            data=data,
            message="Expiry report retrieved successfully.",
            serializer_class=ExpiryReportSerializer,
        )


# ============================================================
# GST REPORT
# ============================================================


class GSTReportView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        data = GSTReportService.get_report(
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "GSTReport",
            retailer.id,
            "Viewed GST Report",
        )

        return self.report_response(
            data=data,
            message="GST report retrieved successfully.",
        )


# ============================================================
# LOW STOCK REPORT
# ============================================================


class LowStockReportView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        data = LowStockReportService.get_report(
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "LowStockReport",
            branch.id if branch else retailer.id,
            "Viewed Low Stock Report",
        )

        return self.report_response(
            data=data,
            message="Low stock report retrieved successfully.",
            serializer_class=LowStockReportSerializer,
        )


# ============================================================
# PAYMENT REPORT
# ============================================================


class PaymentReportView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        data = PaymentReportService.get_report(
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "PaymentReport",
            retailer.id,
            "Viewed Payment Report",
        )

        return self.report_response(
            data=data,
            message="Payment report retrieved successfully.",
        )


# ============================================================
# PRODUCT LEDGER
# ============================================================


class ProductLedgerView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        product_id = self.get_required_param(
            request,
            "product",
        )

        if not product_id:
            return Response(
                {
                    "success": False,
                    "message": "Product ID is required.",
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = ProductLedgerService.get_product_ledger(
            product_id=product_id,
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "ProductLedger",
            product_id,
            f"Viewed Product Ledger for Product {product_id}",
        )

        return self.report_response(
            data=data,
            message="Product ledger retrieved successfully.",
            serializer_class=ProductLedgerSerializer,
        )


# ============================================================
# PROFIT AND LOSS REPORT
# ============================================================


class ProfitLossView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        data = ProfitLossService.get_report(
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "ProfitLossReport",
            branch.id if branch else retailer.id,
            "Viewed Profit and Loss Report",
        )

        return self.report_response(
            data=data,
            message="Profit and loss report retrieved successfully.",
            serializer_class=ProfitLossSerializer,
        )


# ============================================================
# PURCHASE REPORT
# ============================================================


class PurchaseReportView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        data = PurchaseReportService.get_report(
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "PurchaseReport",
            branch.id if branch else retailer.id,
            "Viewed Purchase Report",
        )

        return self.report_response(
            data=data,
            message="Purchase report retrieved successfully.",
            serializer_class=PurchaseReportSerializer,
        )


# ============================================================
# PURCHASE RETURN REPORT
# ============================================================


class PurchaseReturnReportView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        data = PurchaseReturnReportService.get_report(
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "PurchaseReturnReport",
            branch.id if branch else retailer.id,
            "Viewed Purchase Return Report",
        )

        return self.report_response(
            data=data,
            message="Purchase return report retrieved successfully.",
            serializer_class=PurchaseReturnReportSerializer,
        )


# ============================================================
# RECEIPT REPORT
# ============================================================


class ReceiptReportView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        data = ReceiptReportService.get_report(
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "ReceiptReport",
            retailer.id,
            "Viewed Receipt Report",
        )

        return self.report_response(
            data=data,
            message="Receipt report retrieved successfully.",
        )


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
            filters=filters,
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "SalesReport",
            branch.id if branch else retailer.id,
            "Viewed Sales Report",
        )

        return self.report_response(
            data=data,
            message="Sales report retrieved successfully.",
            serializer_class=SalesReportSerializer,
        )


# ============================================================
# SALES RETURN REPORT
# ============================================================


class SalesReturnReportView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        data = SalesReturnReportService.get_report(
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "SalesReturnReport",
            branch.id if branch else retailer.id,
            "Viewed Sales Return Report",
        )

        return self.report_response(
            data=data,
            message="Sales return report retrieved successfully.",
            serializer_class=SalesReturnReportSerializer,
        )


# ============================================================
# STOCK ADJUSTMENT REPORT
# ============================================================


class StockAdjustmentReportView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        data = StockAdjustmentReportService.get_report(
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "StockAdjustmentReport",
            retailer.id,
            "Viewed Stock Adjustment Report",
        )

        return self.report_response(
            data=data,
            message="Stock adjustment report retrieved successfully.",
        )


# ============================================================
# STOCK REPORT
# ============================================================


class StockReportView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        data = StockReportService.get_report(
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "StockReport",
            branch.id if branch else retailer.id,
            "Viewed Stock Report",
        )

        return self.report_response(
            data=data,
            message="Stock report retrieved successfully.",
            serializer_class=StockReportSerializer,
        )


# ============================================================
# STOCK TRANSFER REPORT
# ============================================================


class StockTransferReportView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        data = StockTransferReportService.get_report(
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "StockTransferReport",
            retailer.id,
            "Viewed Stock Transfer Report",
        )

        return self.report_response(
            data=data,
            message="Stock transfer report retrieved successfully.",
        )


# ============================================================
# SUPPLIER LEDGER
# ============================================================


class SupplierLedgerView(BaseReportView):

    def get(self, request):

        retailer, branch = self.get_report_scope(request)

        supplier_id = self.get_required_param(
            request,
            "supplier",
        )

        if not supplier_id:
            return Response(
                {
                    "success": False,
                    "message": "Supplier ID is required.",
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = SupplierLedgerService.get_supplier_ledger(
            supplier_id=supplier_id,
            retailer=retailer,
            branch=branch,
        )

        self.audit_report(
            request,
            "SupplierLedger",
            supplier_id,
            f"Viewed Supplier Ledger for Supplier {supplier_id}",
        )

        return self.report_response(
            data=data,
            message="Supplier ledger retrieved successfully.",
            serializer_class=SupplierLedgerSerializer,
        )
