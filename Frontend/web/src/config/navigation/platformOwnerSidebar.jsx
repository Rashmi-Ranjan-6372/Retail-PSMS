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
  FaSignOutAlt,
  FaKey,
  FaUsers,
  FaCodeBranch,
  FaChartPie,
  FaClipboardCheck,
  FaHistory,
  FaRocket,
  FaSyncAlt,
} from "react-icons/fa";

const platformOwnerSidebar = [
  // Dashboard
  {
    id: "dashboard",
    label: "Dashboard",
    icon: FaTachometerAlt,
    path: "/dashboard",
  },

  // Retailer Management
  {
    id: "retailer-management",
    label: "Retailer Management",
    icon: FaStore,
    children: [
      {
        id: "retailers",
        label: "Retailers",
        icon: FaStore,
        path: "/retailers",
      },
      {
        id: "retailer-requests",
        label: "Retailer Requests",
        icon: FaClipboardCheck,
        path: "/retailers/requests",
      },
      {
        id: "retailer-branches",
        label: "Retailer Branches",
        icon: FaCodeBranch,
        path: "/retailers/branches",
      },
      {
        id: "retailer-users",
        label: "Retailer Users",
        icon: FaUsers,
        path: "/retailers/users",
      },
      {
        id: "retailer-statistics",
        label: "Statistics",
        icon: FaChartPie,
        path: "/retailers/statistics",
      },
    ],
  },

  // Subscription Management
  {
    id: "subscription-management",
    label: "Subscription Management",
    icon: FaCreditCard,
    children: [
      {
        id: "subscription-plans",
        label: "Subscription Plans",
        icon: FaCreditCard,
        path: "/subscriptions/plans",
      },
      {
        id: "retailer-subscriptions",
        label: "Retailer Subscriptions",
        icon: FaStore,
        path: "/subscriptions/retailers",
      },
      {
        id: "trial-subscriptions",
        label: "Trial Subscriptions",
        icon: FaRocket,
        path: "/subscriptions/trials",
      },
      {
        id: "active-subscriptions",
        label: "Active Subscriptions",
        icon: FaClipboardCheck,
        path: "/subscriptions/active",
      },
      {
        id: "expiring-subscriptions",
        label: "Expiring Soon",
        icon: FaHistory,
        path: "/subscriptions/expiring",
      },
      {
        id: "expired-subscriptions",
        label: "Expired Subscriptions",
        icon: FaHistory,
        path: "/subscriptions/expired",
      },
      {
        id: "upgrade-requests",
        label: "Upgrade Requests",
        icon: FaRocket,
        path: "/subscriptions/upgrades",
      },
      {
        id: "renew-subscription",
        label: "Renew Subscription",
        icon: FaSyncAlt,
        path: "/subscriptions/renew",
      },
      {
        id: "subscription-history",
        label: "Subscription History",
        icon: FaHistory,
        path: "/subscriptions/history",
      },
    ],
  },
  // Payment Management
  {
    id: "payment-management",
    label: "Payment Management",
    icon: FaMoneyBillWave,
    children: [
      {
        id: "payment-history",
        label: "Payment History",
        icon: FaMoneyBillWave,
        path: "/payments/history",
      },
      {
        id: "pending-payments",
        label: "Pending Payments",
        icon: FaMoneyBillWave,
        path: "/payments/pending",
      },
      {
        id: "failed-payments",
        label: "Failed Payments",
        icon: FaMoneyBillWave,
        path: "/payments/failed",
      },
      {
        id: "refund-requests",
        label: "Refund Requests",
        icon: FaMoneyBillWave,
        path: "/payments/refunds",
      },
      {
        id: "revenue-report",
        label: "Revenue Report",
        icon: FaChartBar,
        path: "/payments/revenue",
      },
      {
        id: "tax-report",
        label: "Tax Report",
        icon: FaChartBar,
        path: "/payments/tax",
      },
      {
        id: "invoices",
        label: "Invoices",
        icon: FaMoneyBillWave,
        path: "/payments/invoices",
      },
    ],
  },

  // Support Center
  {
    id: "support-center",
    label: "Support Center",
    icon: FaHeadset,
    children: [
      {
        id: "support-tickets",
        label: "Support Tickets",
        icon: FaHeadset,
        path: "/support/tickets",
      },
      {
        id: "open-tickets",
        label: "Open Tickets",
        icon: FaHeadset,
        path: "/support/open",
      },
      {
        id: "tickets-in-progress",
        label: "In Progress",
        icon: FaHeadset,
        path: "/support/in-progress",
      },
      {
        id: "closed-tickets",
        label: "Closed Tickets",
        icon: FaHeadset,
        path: "/support/closed",
      },
      {
        id: "ticket-categories",
        label: "Ticket Categories",
        icon: FaHeadset,
        path: "/support/categories",
      },
      {
        id: "ticket-analytics",
        label: "Ticket Analytics",
        icon: FaChartBar,
        path: "/support/analytics",
      },
    ],
  },

  // Backup & Recovery
  {
    id: "backup",
    label: "Backup & Recovery",
    icon: FaDatabase,
    children: [
      {
        id: "create-backup",
        label: "Create Backup",
        icon: FaDatabase,
        path: "/backup/create",
      },
      {
        id: "backup-history",
        label: "Backup History",
        icon: FaDatabase,
        path: "/backup/history",
      },
      {
        id: "download-backup",
        label: "Download Backup",
        icon: FaDatabase,
        path: "/backup/download",
      },
      {
        id: "restore-backup",
        label: "Restore Backup",
        icon: FaDatabase,
        path: "/backup/restore",
      },
      {
        id: "backup-schedule",
        label: "Backup Schedule",
        icon: FaDatabase,
        path: "/backup/schedule",
      },
      {
        id: "storage-usage",
        label: "Storage Usage",
        icon: FaDatabase,
        path: "/backup/storage",
      },
    ],
  },

  // Audit & Security
  {
    id: "audit",
    label: "Audit & Security",
    icon: FaShieldAlt,
    children: [
      {
        id: "audit-logs",
        label: "Audit Logs",
        icon: FaShieldAlt,
        path: "/audit/logs",
      },
      {
        id: "login-logs",
        label: "Login Logs",
        icon: FaShieldAlt,
        path: "/audit/login-logs",
      },
      {
        id: "user-sessions",
        label: "User Sessions",
        icon: FaShieldAlt,
        path: "/audit/sessions",
      },
      {
        id: "failed-login-attempts",
        label: "Failed Login Attempts",
        icon: FaShieldAlt,
        path: "/audit/failed-logins",
      },
      {
        id: "locked-accounts",
        label: "Locked Accounts",
        icon: FaShieldAlt,
        path: "/audit/locked-accounts",
      },
      {
        id: "security-reports",
        label: "Security Reports",
        icon: FaChartBar,
        path: "/audit/security-reports",
      },
      {
        id: "api-logs",
        label: "API Logs",
        icon: FaShieldAlt,
        path: "/audit/api-logs",
      },
      {
        id: "activity-timeline",
        label: "Activity Timeline",
        icon: FaChartBar,
        path: "/audit/activity",
      },
    ],
  },
  // Notifications
  {
    id: "notifications",
    label: "Notifications",
    icon: FaBell,
    children: [
      {
        id: "announcements",
        label: "Announcements",
        icon: FaBell,
        path: "/notifications/announcements",
      },
      {
        id: "email-broadcast",
        label: "Email Broadcast",
        icon: FaBell,
        path: "/notifications/email",
      },
      {
        id: "sms-notifications",
        label: "SMS Notifications",
        icon: FaBell,
        path: "/notifications/sms",
      },
      {
        id: "subscription-alerts",
        label: "Subscription Alerts",
        icon: FaBell,
        path: "/notifications/subscription-alerts",
      },
      {
        id: "system-notifications",
        label: "System Notifications",
        icon: FaBell,
        path: "/notifications/system",
      },
      {
        id: "notification-templates",
        label: "Notification Templates",
        icon: FaBell,
        path: "/notifications/templates",
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
        id: "retailer-report",
        label: "Retailer Report",
        icon: FaChartBar,
        path: "/reports/retailers",
      },
      {
        id: "subscription-report",
        label: "Subscription Report",
        icon: FaChartBar,
        path: "/reports/subscriptions",
      },
      {
        id: "revenue-report",
        label: "Revenue Report",
        icon: FaChartBar,
        path: "/reports/revenue",
      },
      {
        id: "payment-report",
        label: "Payment Report",
        icon: FaChartBar,
        path: "/reports/payments",
      },
      {
        id: "user-report",
        label: "User Report",
        icon: FaChartBar,
        path: "/reports/users",
      },
      {
        id: "audit-report",
        label: "Audit Report",
        icon: FaChartBar,
        path: "/reports/audit",
      },
      {
        id: "backup-report",
        label: "Backup Report",
        icon: FaChartBar,
        path: "/reports/backups",
      },
      {
        id: "system-report",
        label: "System Report",
        icon: FaChartBar,
        path: "/reports/system",
      },
    ],
  },

  // System Settings
  {
    id: "system-settings",
    label: "System Settings",
    icon: FaCog,
    children: [
      {
        id: "platform-settings",
        label: "Platform Settings",
        icon: FaCog,
        path: "/settings/platform",
      },
      {
        id: "smtp-settings",
        label: "SMTP Settings",
        icon: FaCog,
        path: "/settings/smtp",
      },
      {
        id: "sms-settings",
        label: "SMS Settings",
        icon: FaCog,
        path: "/settings/sms",
      },
      {
        id: "backup-settings",
        label: "Backup Settings",
        icon: FaDatabase,
        path: "/settings/backup",
      },
      {
        id: "storage-settings",
        label: "Storage Settings",
        icon: FaDatabase,
        path: "/settings/storage",
      },
      {
        id: "api-settings",
        label: "API Settings",
        icon: FaCog,
        path: "/settings/api",
      },
      {
        id: "maintenance-mode",
        label: "Maintenance Mode",
        icon: FaCog,
        path: "/settings/maintenance",
      },
      {
        id: "system-configuration",
        label: "System Configuration",
        icon: FaCog,
        path: "/settings/configuration",
      },
      {
        id: "license-management",
        label: "License Management",
        icon: FaCog,
        path: "/settings/license",
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
        id: "activity-log",
        label: "Activity Log",
        icon: FaChartBar,
        path: "/account/activity",
      },
      {
        id: "notification-settings",
        label: "Notification Settings",
        icon: FaBell,
        path: "/account/notifications",
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

export default platformOwnerSidebar;
