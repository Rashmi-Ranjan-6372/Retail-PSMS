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
  FaPercentage,
  FaUserCircle,
  FaSignOutAlt,
} from "react-icons/fa";

const storeManagerSidebar = [
  // Dashboard
  {
    id: "dashboard",
    label: "Dashboard",
    icon: FaTachometerAlt,
    path: "/dashboard",
  },

  // Masters
  {
    id: "masters",
    label: "Masters",
    icon: FaBoxes,
    children: [
      {
        label: "Products",
        icon: FaCapsules,
        path: "/masters/products",
      },
      {
        label: "Categories",
        icon: FaBoxes,
        path: "/masters/categories",
      },
      {
        label: "Manufacturers",
        icon: FaIndustry,
        path: "/masters/manufacturers",
      },
      {
        label: "Suppliers",
        icon: FaTruck,
        path: "/masters/suppliers",
      },
      {
        label: "Customers",
        icon: FaUserFriends,
        path: "/masters/customers",
      },
      {
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
        label: "Stock Transactions",
        path: "/inventory/transactions",
      },
      {
        label: "Stock Batches",
        path: "/inventory/batches",
      },
      {
        label: "Stock Adjustments",
        path: "/inventory/adjustments",
      },
      {
        label: "Stock Transfers",
        path: "/inventory/transfers",
      },
      {
        label: "Expiry Damages",
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
        label: "Purchases",
        icon: FaFileInvoice,
        path: "/purchases",
      },
      {
        label: "Purchase Returns",
        icon: FaUndo,
        path: "/purchase-returns",
      },
      {
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
        label: "Sales",
        path: "/sales",
      },
      {
        label: "Sales Returns",
        path: "/sales-returns",
      },
      {
        label: "Receipts",
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
        label: "Sales Report",
        path: "/reports/sales",
      },
      {
        label: "Purchase Report",
        path: "/reports/purchases",
      },
      {
        label: "Stock Report",
        path: "/reports/stock",
      },
      {
        label: "Profit & Loss",
        path: "/reports/profit-loss",
      },
      {
        label: "Expiry Report",
        path: "/reports/expiry",
      },
      {
        label: "Low Stock Report",
        path: "/reports/low-stock",
      },
      {
        label: "Customer Ledger",
        path: "/reports/customer-ledger",
      },
      {
        label: "Supplier Ledger",
        path: "/reports/supplier-ledger",
      },
      {
        label: "Product Ledger",
        path: "/reports/product-ledger",
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
        label: "Profile",
        path: "/account/profile",
      },
      {
        label: "Change Password",
        path: "/account/change-password",
      },
      {
        label: "Logout",
        icon: FaSignOutAlt,
        path: "/logout",
      },
    ],
  },
];

export default storeManagerSidebar;