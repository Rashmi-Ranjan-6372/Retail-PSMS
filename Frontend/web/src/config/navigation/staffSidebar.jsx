import {
  FaTachometerAlt,
  FaWarehouse,
  FaBoxes,
  FaChartBar,
  FaClipboardList,
  FaUserCircle,
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
        label: "View Stock",
        icon: FaBoxes,
        path: "/inventory/view-stock",
      },
      {
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
        label: "Stock Report",
        icon: FaClipboardList,
        path: "/reports/stock",
      },
      {
        label: "Low Stock Report",
        icon: FaClipboardList,
        path: "/reports/low-stock",
      },
      {
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

export default staffSidebar;