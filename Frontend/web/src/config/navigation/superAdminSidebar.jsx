// src/config/sidebar/superAdminSidebar.js

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
  FaMapMarkedAlt,
  FaUsers,
  FaCog,
  FaCalendarAlt,
  FaPercentage,
  FaDatabase,
  FaUserCircle,
  FaSignOutAlt,
} from "react-icons/fa";

const superAdminSidebar = [
  {
    id: "dashboard",
    label: "Dashboard",
    icon: FaTachometerAlt,
    path: "/dashboard",
  },

  // ===========================
  // Masters
  // ===========================

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

  // ===========================
  // Inventory
  // ===========================

  {
    id: "inventory",
    label: "Inventory",
    icon: FaWarehouse,
    children: [
      {
        id: "stock-transactions",
        label: "Stock Transactions",
        icon: FaBoxes,
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
        icon: FaUndo,
        path: "/inventory/adjustments",
      },
      {
        id: "stock-transfers",
        label: "Stock Transfers",
        icon: FaUndo,
        path: "/inventory/transfers",
      },
      {
        id: "expiry-damages",
        label: "Expiry Damages",
        icon: FaUndo,
        path: "/inventory/expiry-damages",
      },
    ],
  },

  // ===========================
  // Purchases
  // ===========================

  {
    id: "purchases",
    label: "Purchases",
    icon: FaTruck,
    children: [
      {
        id: "purchase-list",
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

  // ===========================
  // Sales
  // ===========================

  {
    id: "sales",
    label: "Sales",
    icon: FaFileInvoiceDollar,
    children: [
      {
        id: "sales-list",
        label: "Sales",
        icon: FaFileInvoiceDollar,
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

  // ===========================
  // Reports
  // ===========================

  {
    id: "reports",
    label: "Reports",
    icon: FaChartBar,
    children: [
      {
        id: "sales-report",
        label: "Sales Report",
        path: "/reports/sales",
      },
      {
        id: "purchase-report",
        label: "Purchase Report",
        path: "/reports/purchases",
      },
      {
        id: "stock-report",
        label: "Stock Report",
        path: "/reports/stock",
      },
      {
        id: "profit-loss",
        label: "Profit & Loss",
        path: "/reports/profit-loss",
      },
      {
        id: "expiry-report",
        label: "Expiry Report",
        path: "/reports/expiry",
      },
      {
        id: "low-stock-report",
        label: "Low Stock Report",
        path: "/reports/low-stock",
      },
      {
        id: "customer-ledger",
        label: "Customer Ledger",
        path: "/reports/customer-ledger",
      },
      {
        id: "supplier-ledger",
        label: "Supplier Ledger",
        path: "/reports/supplier-ledger",
      },
      {
        id: "product-ledger",
        label: "Product Ledger",
        path: "/reports/product-ledger",
      },
    ],
  },

  // ===========================
  // Branch Management
  // ===========================

  {
    id: "branches",
    label: "Branch Management",
    icon: FaMapMarkedAlt,
    children: [
      {
        id: "branch-list",
        label: "Branches",
        path: "/branches",
      },
    ],
  },
  // ===========================
  // User Management
  // ===========================

  {
    id: "users",
    label: "User Management",
    icon: FaUsers,
    children: [
      {
        id: "users-list",
        label: "Users",
        path: "/users",
      },
      {
        id: "user-sessions",
        label: "User Sessions",
        path: "/users/sessions",
      },
      {
        id: "login-logs",
        label: "Login Logs",
        path: "/users/login-logs",
      },
      {
        id: "audit-logs",
        label: "Audit Logs",
        path: "/users/audit-logs",
      },
    ],
  },

  // ===========================
  // Settings
  // ===========================

  {
    id: "settings",
    label: "Settings",
    icon: FaCog,
    children: [
      {
        id: "general-settings",
        label: "General Settings",
        path: "/settings/general",
      },
      {
        id: "financial-years",
        label: "Financial Years",
        icon: FaCalendarAlt,
        path: "/settings/financial-years",
      },
      {
        id: "tax-settings",
        label: "GST / Tax Settings",
        icon: FaPercentage,
        path: "/settings/tax",
      },
      {
        id: "backup-management",
        label: "Backup Management",
        icon: FaDatabase,
        children: [
          {
            id: "create-backup",
            label: "Create Backup",
            path: "/settings/backup/create",
          },
          {
            id: "backup-history",
            label: "Backup History",
            path: "/settings/backup/history",
          },
          {
            id: "restore-backup",
            label: "Restore Backup",
            path: "/settings/backup/restore",
          },
          {
            id: "backup-schedule",
            label: "Backup Schedule",
            path: "/settings/backup/schedule",
          },
        ],
      },
      {
        id: "system-preferences",
        label: "System Preferences",
        path: "/settings/preferences",
      },
    ],
  },

  // ===========================
  // Account
  // ===========================

  {
    id: "account",
    label: "Account",
    icon: FaUserCircle,
    children: [
      {
        id: "profile",
        label: "Profile",
        path: "/account/profile",
      },
      {
        id: "change-password",
        label: "Change Password",
        path: "/account/change-password",
      },
      {
        id: "logout",
        label: "Logout",
        icon: FaSignOutAlt,
        path: "/logout",
      },
    ],
  },
];

export default superAdminSidebar;
