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

  // ===========================
  // Inventory
  // ===========================

  {
    id: "inventory",
    label: "Inventory",
    icon: FaWarehouse,
    children: [
      {
        label: "Stock Transactions",
        icon: FaBoxes,
        path: "/inventory/transactions",
      },
      {
        label: "Stock Batches",
        icon: FaBoxes,
        path: "/inventory/batches",
      },
      {
        label: "Stock Adjustments",
        icon: FaUndo,
        path: "/inventory/adjustments",
      },
      {
        label: "Stock Transfers",
        icon: FaUndo,
        path: "/inventory/transfers",
      },
      {
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

  // ===========================
  // Sales
  // ===========================

  {
    id: "sales",
    label: "Sales",
    icon: FaFileInvoiceDollar,
    children: [
      {
        label: "Sales",
        icon: FaFileInvoiceDollar,
        path: "/sales",
      },
      {
        label: "Sales Returns",
        icon: FaUndo,
        path: "/sales-returns",
      },
      {
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

  // ===========================
  // Branch Management
  // ===========================

  {
    id: "branches",
    label: "Branch Management",
    icon: FaMapMarkedAlt,
    children: [
      {
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
        label: "Users",
        path: "/users",
      },
      {
        label: "User Sessions",
        path: "/users/sessions",
      },
      {
        label: "Login Logs",
        path: "/users/login-logs",
      },
      {
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
      label: "General Settings",
      path: "/settings/general",
    },
    {
      label: "Financial Years",
      icon: FaCalendarAlt,
      path: "/settings/financial-years",
    },
    {
      label: "GST / Tax Settings",
      icon: FaPercentage,
      path: "/settings/tax",
    },

    {
      label: "Backup Management",
      icon: FaDatabase,
      children: [
        {
          label: "Create Backup",
          path: "/settings/backup/create",
        },
        {
          label: "Backup History",
          path: "/settings/backup/history",
        },
        {
          label: "Restore Backup",
          path: "/settings/backup/restore",
        },
        {
          label: "Backup Schedule",
          path: "/settings/backup/schedule",
        },
      ],
    },

    {
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

export default superAdminSidebar;