import {
  FaTachometerAlt,
  FaBoxes,
  FaCapsules,
  FaIndustry,
  FaTruck,
  FaUserFriends,
  FaWarehouse,
  FaUndo,
  FaMoneyCheckAlt,
  FaFileInvoice,
  FaFileInvoiceDollar,
  FaChartBar,
  FaUsers,
  FaPercentage,
  FaUserCircle,
  FaSignOutAlt,
  FaClipboardList,
  FaExchangeAlt,
  FaExclamationTriangle,
  FaChartLine,
  FaUserClock,
  FaHistory,
  FaUserEdit,
  FaKey,
  FaReceipt,
} from "react-icons/fa";

const adminSidebar = [
  // Dashboard
  {
    id: "dashboard",
    label: "Dashboard",
    icon: FaTachometerAlt,
    path: "/dashboard",
    exact: true,
  },

  // Masters
  {
    id: "masters",
    label: "Masters",
    icon: FaBoxes,
    children: [
      {
        id: "products",
        label: "Products",
        icon: FaCapsules,
        path: "/masters/products",
      },
      {
        id: "categories",
        label: "Categories",
        icon: FaBoxes,
        path: "/masters/categories",
      },
      {
        id: "manufacturers",
        label: "Manufacturers",
        icon: FaIndustry,
        path: "/masters/manufacturers",
      },
      {
        id: "suppliers",
        label: "Suppliers",
        icon: FaTruck,
        path: "/masters/suppliers",
      },
      {
        id: "customers",
        label: "Customers",
        icon: FaUserFriends,
        path: "/masters/customers",
      },
      {
        id: "sales-offers",
        label: "Sales Offers",
        icon: FaPercentage,
        path: "/masters/sales-offers",
      },
    ],
  },

  // Inventory
  {
    id: "inventory",
    label: "Inventory",
    icon: FaWarehouse,
    children: [
      {
        id: "stock-transactions",
        label: "Stock Transactions",
        icon: FaClipboardList,
        path: "/inventory/transactions",
      },
      {
        id: "stock-batches",
        label: "Stock Batches",
        icon: FaBoxes,
        path: "/inventory/batches",
      },
      {
        id: "stock-adjustments",
        label: "Stock Adjustments",
        icon: FaExchangeAlt,
        path: "/inventory/adjustments",
      },
      {
        id: "stock-transfers",
        label: "Stock Transfers",
        icon: FaExchangeAlt,
        path: "/inventory/transfers",
      },
      {
        id: "expiry-damages",
        label: "Expiry Damages",
        icon: FaExclamationTriangle,
        path: "/inventory/expiry-damages",
      },
    ],
  },

  // Purchases
  {
    id: "purchases",
    label: "Purchases",
    icon: FaTruck,
    children: [
      {
        id: "purchases-list",
        label: "Purchases",
        icon: FaFileInvoice,
        path: "/purchases",
      },
      {
        id: "purchase-returns",
        label: "Purchase Returns",
        icon: FaUndo,
        path: "/purchase-returns",
      },
      {
        id: "purchase-payments",
        label: "Payments",
        icon: FaMoneyCheckAlt,
        path: "/purchase-payments",
      },
    ],
  },

  // Sales
  {
    id: "sales",
    label: "Sales",
    icon: FaFileInvoiceDollar,
    children: [
      {
        id: "sales-list",
        label: "Sales",
        icon: FaReceipt,
        path: "/sales",
      },
      {
        id: "sales-returns",
        label: "Sales Returns",
        icon: FaUndo,
        path: "/sales-returns",
      },
      {
        id: "receipts",
        label: "Receipts",
        icon: FaMoneyCheckAlt,
        path: "/receipts",
      },
    ],
  },

  // Reports
  {
    id: "reports",
    label: "Reports",
    icon: FaChartBar,
    children: [
      {
        id: "sales-report",
        label: "Sales Report",
        icon: FaChartLine,
        path: "/reports/sales",
      },
      {
        id: "purchase-report",
        label: "Purchase Report",
        icon: FaChartLine,
        path: "/reports/purchases",
      },
      {
        id: "stock-report",
        label: "Stock Report",
        icon: FaWarehouse,
        path: "/reports/stock",
      },
      {
        id: "profit-loss",
        label: "Profit & Loss",
        icon: FaChartBar,
        path: "/reports/profit-loss",
      },
      {
        id: "expiry-report",
        label: "Expiry Report",
        icon: FaExclamationTriangle,
        path: "/reports/expiry",
      },
      {
        id: "low-stock-report",
        label: "Low Stock Report",
        icon: FaBoxes,
        path: "/reports/low-stock",
      },
      {
        id: "customer-ledger",
        label: "Customer Ledger",
        icon: FaUserFriends,
        path: "/reports/customer-ledger",
      },
      {
        id: "supplier-ledger",
        label: "Supplier Ledger",
        icon: FaTruck,
        path: "/reports/supplier-ledger",
      },
      {
        id: "product-ledger",
        label: "Product Ledger",
        icon: FaCapsules,
        path: "/reports/product-ledger",
      },
    ],
  },

  // User Management
  {
    id: "users",
    label: "User Management",
    icon: FaUsers,
    children: [
      {
        id: "users-list",
        label: "Users",
        icon: FaUsers,
        path: "/users",
      },
      {
        id: "user-sessions",
        label: "User Sessions",
        icon: FaUserClock,
        path: "/users/sessions",
      },
      {
        id: "login-logs",
        label: "Login Logs",
        icon: FaHistory,
        path: "/users/login-logs",
      },
      {
        id: "audit-logs",
        label: "Audit Logs",
        icon: FaClipboardList,
        path: "/users/audit-logs",
      },
    ],
  },

  // Account
  {
    id: "account",
    label: "Account",
    icon: FaUserCircle,
    children: [
      {
        id: "profile",
        label: "Profile",
        icon: FaUserEdit,
        path: "/account/profile",
      },
      {
        id: "change-password",
        label: "Change Password",
        icon: FaKey,
        path: "/account/change-password",
      },
      {
        id: "logout",
        label: "Logout",
        icon: FaSignOutAlt,
        action: "logout",
      },
    ],
  },
];

export default adminSidebar;
