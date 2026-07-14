import {
  FaTachometerAlt,
  FaBoxes,
  FaCapsules,
  FaUserFriends,
  FaWarehouse,
  FaClock,
  FaFileInvoiceDollar,
  FaUndo,
  FaMoneyCheckAlt,
  FaChartBar,
  FaClipboardList,
  FaUserCircle,
  FaKey,
  FaSignOutAlt,
} from "react-icons/fa";

const pharmacistSidebar = [
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
        id: "customers",
        label: "Customers",
        icon: FaUserFriends,
        path: "/masters/customers",
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
        icon: FaWarehouse,
        path: "/inventory/transactions",
      },
      {
        id: "stock-batches",
        label: "Stock Batches",
        icon: FaWarehouse,
        path: "/inventory/batches",
      },
      {
        id: "expiry-damages",
        label: "Expiry Damages",
        icon: FaClock,
        path: "/inventory/expiry-damages",
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

  // Reports
  {
    id: "reports",
    label: "Reports",
    icon: FaChartBar,
    children: [
      {
        id: "stock-report",
        label: "Stock Report",
        icon: FaWarehouse,
        path: "/reports/stock",
      },
      {
        id: "expiry-report",
        label: "Expiry Report",
        icon: FaClock,
        path: "/reports/expiry",
      },
      {
        id: "product-ledger",
        label: "Product Ledger",
        icon: FaClipboardList,
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
        id: "profile",
        label: "Profile",
        icon: FaUserCircle,
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
        path: "/logout",
      },
    ],
  },
];

export default pharmacistSidebar;
