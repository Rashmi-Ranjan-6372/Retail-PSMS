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
        label: "Stock Transactions",
        path: "/inventory/transactions",
      },
      {
        label: "Stock Batches",
        path: "/inventory/batches",
      },
      {
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
        label: "Sales",
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

  // Reports
  {
    id: "reports",
    label: "Reports",
    icon: FaChartBar,
    children: [
      {
        label: "Stock Report",
        icon: FaWarehouse,
        path: "/reports/stock",
      },
      {
        label: "Expiry Report",
        icon: FaClock,
        path: "/reports/expiry",
      },
      {
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

export default pharmacistSidebar;