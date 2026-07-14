import {
  FaTachometerAlt,
  FaFileInvoiceDollar,
  FaUndo,
  FaMoneyCheckAlt,
  FaUserFriends,
  FaChartBar,
  FaUserCircle,
  FaSignOutAlt,
  FaReceipt,
  FaChartLine,
  FaUserEdit,
  FaKey,
} from "react-icons/fa";

const cashierSidebar = [
  // Dashboard
  {
    id: "dashboard",
    label: "Dashboard",
    icon: FaTachometerAlt,
    path: "/dashboard",
    exact: true,
  },

  // Sales
  {
    id: "sales",
    label: "Sales",
    icon: FaFileInvoiceDollar,
    children: [
      {
        id: "sales",
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

  // Customers
  {
    id: "customers",
    label: "Customers",
    icon: FaUserFriends,
    path: "/masters/customers",
  },

  // Reports
  {
    id: "reports",
    label: "Reports",
    icon: FaChartBar,
    children: [
      {
        id: "daily-sales-summary",
        label: "Daily Sales Summary",
        icon: FaChartLine,
        path: "/reports/daily-sales",
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

export default cashierSidebar;
