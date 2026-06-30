import {
  FaTachometerAlt,
  FaFileInvoiceDollar,
  FaUndo,
  FaMoneyCheckAlt,
  FaUserFriends,
  FaChartBar,
  FaUserCircle,
  FaSignOutAlt,
} from "react-icons/fa";

const cashierSidebar = [
  // Dashboard
  {
    id: "dashboard",
    label: "Dashboard",
    icon: FaTachometerAlt,
    path: "/dashboard",
  },

  // Sales
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
        label: "Daily Sales Summary",
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

export default cashierSidebar;