// src/config/sidebar/platformOwnerSidebar.jsx

import {
  FaTachometerAlt,
  FaStore,
  FaCreditCard,
  FaMoneyBillWave,
  FaHeadset,
  FaDatabase,
  FaShieldAlt,
  FaBell,
  FaChartBar,
  FaCog,
  FaUserCircle,
} from "react-icons/fa";

const platformOwnerSidebar = [
  {
    id: "dashboard",
    label: "Dashboard",
    icon: FaTachometerAlt,
    path: "/dashboard",
  },

  {
    id: "retailer-management",
    label: "Retailer Management",
    icon: FaStore,
    children: [
      {
        label: "Retailers",
        path: "/retailers",
      },
      {
        label: "Retailer Requests",
        path: "/retailers/requests",
      },
      {
        label: "Active Retailers",
        path: "/retailers/active",
      },
      {
        label: "Suspended Retailers",
        path: "/retailers/suspended",
      },
      {
        label: "Expired Retailers",
        path: "/retailers/expired",
      },
      {
        label: "Retailer Branches",
        path: "/retailers/branches",
      },
      {
        label: "Retailer Users",
        path: "/retailers/users",
      },
      {
        label: "Retailer Statistics",
        path: "/retailers/statistics",
      },
    ],
  },

  {
    id: "subscription-management",
    label: "Subscription Management",
    icon: FaCreditCard,
    children: [
      {
        label: "Subscription Plans",
        path: "/subscriptions/plans",
      },
      {
        label: "Retailer Subscriptions",
        path: "/subscriptions/retailers",
      },
      {
        label: "Trial Subscriptions",
        path: "/subscriptions/trials",
      },
      {
        label: "Active Subscriptions",
        path: "/subscriptions/active",
      },
      {
        label: "Expiring Soon",
        path: "/subscriptions/expiring",
      },
      {
        label: "Expired Subscriptions",
        path: "/subscriptions/expired",
      },
      {
        label: "Upgrade Requests",
        path: "/subscriptions/upgrades",
      },
      {
        label: "Renew Subscription",
        path: "/subscriptions/renew",
      },
      {
        label: "Subscription History",
        path: "/subscriptions/history",
      },
    ],
  },

  {
    id: "payment-management",
    label: "Payment Management",
    icon: FaMoneyBillWave,
    children: [
      {
        label: "Payment History",
        path: "/payments/history",
      },
      {
        label: "Pending Payments",
        path: "/payments/pending",
      },
      {
        label: "Failed Payments",
        path: "/payments/failed",
      },
      {
        label: "Refund Requests",
        path: "/payments/refunds",
      },
      {
        label: "Revenue Report",
        path: "/payments/revenue",
      },
      {
        label: "Tax Report",
        path: "/payments/tax",
      },
      {
        label: "Invoices",
        path: "/payments/invoices",
      },
    ],
  },

  {
    id: "support-center",
    label: "Support Center",
    icon: FaHeadset,
    children: [
      {
        label: "Support Tickets",
        path: "/support/tickets",
      },
      {
        label: "Open Tickets",
        path: "/support/open",
      },
      {
        label: "In Progress",
        path: "/support/in-progress",
      },
      {
        label: "Closed Tickets",
        path: "/support/closed",
      },
      {
        label: "Ticket Categories",
        path: "/support/categories",
      },
      {
        label: "Ticket Analytics",
        path: "/support/analytics",
      },
    ],
  },

  {
    id: "backup",
    label: "Backup & Recovery",
    icon: FaDatabase,
    children: [
      {
        label: "Create Backup",
        path: "/backup/create",
      },
      {
        label: "Backup History",
        path: "/backup/history",
      },
      {
        label: "Download Backup",
        path: "/backup/download",
      },
      {
        label: "Restore Backup",
        path: "/backup/restore",
      },
      {
        label: "Backup Schedule",
        path: "/backup/schedule",
      },
      {
        label: "Storage Usage",
        path: "/backup/storage",
      },
    ],
  },

  {
    id: "audit",
    label: "Audit & Security",
    icon: FaShieldAlt,
    children: [
      {
        label: "Audit Logs",
        path: "/audit/logs",
      },
      {
        label: "Login Logs",
        path: "/audit/login-logs",
      },
      {
        label: "User Sessions",
        path: "/audit/sessions",
      },
      {
        label: "Failed Login Attempts",
        path: "/audit/failed-logins",
      },
      {
        label: "Locked Accounts",
        path: "/audit/locked-accounts",
      },
      {
        label: "Security Reports",
        path: "/audit/security-reports",
      },
      {
        label: "API Logs",
        path: "/audit/api-logs",
      },
      {
        label: "Activity Timeline",
        path: "/audit/activity",
      },
    ],
  },

  {
    id: "notifications",
    label: "Notifications",
    icon: FaBell,
    children: [
      {
        label: "Announcements",
        path: "/notifications/announcements",
      },
      {
        label: "Email Broadcast",
        path: "/notifications/email",
      },
      {
        label: "SMS Notifications",
        path: "/notifications/sms",
      },
      {
        label: "Subscription Alerts",
        path: "/notifications/subscription-alerts",
      },
      {
        label: "System Notifications",
        path: "/notifications/system",
      },
      {
        label: "Notification Templates",
        path: "/notifications/templates",
      },
    ],
  },

  {
    id: "reports",
    label: "Reports",
    icon: FaChartBar,
    children: [
      {
        label: "Retailer Report",
        path: "/reports/retailers",
      },
      {
        label: "Subscription Report",
        path: "/reports/subscriptions",
      },
      {
        label: "Revenue Report",
        path: "/reports/revenue",
      },
      {
        label: "Payment Report",
        path: "/reports/payments",
      },
      {
        label: "User Report",
        path: "/reports/users",
      },
      {
        label: "Audit Report",
        path: "/reports/audit",
      },
      {
        label: "Backup Report",
        path: "/reports/backups",
      },
      {
        label: "System Report",
        path: "/reports/system",
      },
    ],
  },

  {
    id: "system-settings",
    label: "System Settings",
    icon: FaCog,
    children: [
      {
        label: "Platform Settings",
        path: "/settings/platform",
      },
      {
        label: "SMTP Settings",
        path: "/settings/smtp",
      },
      {
        label: "SMS Settings",
        path: "/settings/sms",
      },
      {
        label: "Backup Settings",
        path: "/settings/backup",
      },
      {
        label: "Storage Settings",
        path: "/settings/storage",
      },
      {
        label: "API Settings",
        path: "/settings/api",
      },
      {
        label: "Maintenance Mode",
        path: "/settings/maintenance",
      },
      {
        label: "System Configuration",
        path: "/settings/configuration",
      },
      {
        label: "License Management",
        path: "/settings/license",
      },
    ],
  },

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
        label: "Activity Log",
        path: "/account/activity",
      },
      {
        label: "Notification Settings",
        path: "/account/notifications",
      },
      {
        label: "Logout",
        path: "/logout",
      },
    ],
  },
];

export default platformOwnerSidebar;