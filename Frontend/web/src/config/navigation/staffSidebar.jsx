import {
  FaTachometerAlt,
  FaWarehouse,
  FaBoxes,
  FaChartBar,
  FaClipboardList,
  FaUserCircle,
  FaKey,
  FaSignOutAlt,
} from "react-icons/fa";

const staffSidebar = [
  // Dashboard
  {
    id: "dashboard",
    label: "Dashboard",
    icon: FaTachometerAlt,
    path: "/dashboard",
  },

  // Inventory
  {
    id: "inventory",
    label: "Inventory",
    icon: FaWarehouse,
    children: [
      {
        id: "view-stock",
        label: "View Stock",
        icon: FaBoxes,
        path: "/inventory/view-stock",
      },
      {
        id: "stock-batches",
        label: "Stock Batches",
        icon: FaBoxes,
        path: "/inventory/batches",
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
        icon: FaClipboardList,
        path: "/reports/stock",
      },
      {
        id: "low-stock-report",
        label: "Low Stock Report",
        icon: FaClipboardList,
        path: "/reports/low-stock",
      },
      {
        id: "expiry-report",
        label: "Expiry Report",
        icon: FaClipboardList,
        path: "/reports/expiry",
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

export default staffSidebar;