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
        id: "retailers",
        label: "Retailers",
        path: "/retailers",
      },
      {
        id: "retailer-requests",
        label: "Retailer Requests",
        path: "/retailers/requests",
      },
      {
        id: "active-retailers",
        label: "Active Retailers",
        path: "/retailers/active",
      },
      {
        id: "suspended-retailers",
        label: "Suspended Retailers",
        path: "/retailers/suspended",
      },
      {
        id: "expired-retailers",
        label: "Expired Retailers",
        path: "/retailers/expired",
      },
      {
        id: "retailer-branches",
        label: "Retailer Branches",
        path: "/retailers/branches",
      },
      {
        id: "retailer-users",
        label: "Retailer Users",
        path: "/retailers/users",
      },
      {
        id: "retailer-statistics",
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
        id: "subscription-plans",
        label: "Subscription Plans",
        path: "/subscriptions/plans",
      },
      {
        id: "retailer-subscriptions",
        label: "Retailer Subscriptions",
        path: "/subscriptions/retailers",
      },
      {
        id: "trial-subscriptions",
        label: "Trial Subscriptions",
        path: "/subscriptions/trials",
      },
      {
        id: "active-subscriptions",
        label: "Active Subscriptions",
        path: "/subscriptions/active",
      },
      {
        id: "expiring-subscriptions",
        label: "Expiring Soon",
        path: "/subscriptions/expiring",
      },
      {
        id: "expired-subscriptions",
        label: "Expired Subscriptions",
        path: "/subscriptions/expired",
      },
      {
        id: "upgrade-requests",
        label: "Upgrade Requests",
        path: "/subscriptions/upgrades",
      },
      {
        id: "renew-subscription",
        label: "Renew Subscription",
        path: "/subscriptions/renew",
      },
      {
        id: "subscription-history",
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
        id: "payment-history",
        label: "Payment History",
        path: "/payments/history",
      },
      {
        id: "pending-payments",
        label: "Pending Payments",
        path: "/payments/pending",
      },
      {
        id: "failed-payments",
        label: "Failed Payments",
        path: "/payments/failed",
      },
      {
        id: "refund-requests",
        label: "Refund Requests",
        path: "/payments/refunds",
      },
      {
        id: "revenue-report",
        label: "Revenue Report",
        path: "/payments/revenue",
      },
      {
        id: "tax-report",
        label: "Tax Report",
        path: "/payments/tax",
      },
      {
        id: "invoices",
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
        id: "support-tickets",
        label: "Support Tickets",
        path: "/support/tickets",
      },
      {
        id: "open-tickets",
        label: "Open Tickets",
        path: "/support/open",
      },
      {
        id: "tickets-in-progress",
        label: "In Progress",
        path: "/support/in-progress",
      },
      {
        id: "closed-tickets",
        label: "Closed Tickets",
        path: "/support/closed",
      },
      {
        id: "ticket-categories",
        label: "Ticket Categories",
        path: "/support/categories",
      },
      {
        id: "ticket-analytics",
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
        id: "create-backup",
        label: "Create Backup",
        path: "/backup/create",
      },
      {
        id: "backup-history",
        label: "Backup History",
        path: "/backup/history",
      },
      {
        id: "download-backup",
        label: "Download Backup",
        path: "/backup/download",
      },
      {
        id: "restore-backup",
        label: "Restore Backup",
        path: "/backup/restore",
      },
      {
        id: "backup-schedule",
        label: "Backup Schedule",
        path: "/backup/schedule",
      },
      {
        id: "storage-usage",
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
        id: "audit-logs",
        label: "Audit Logs",
        path: "/audit/logs",
      },
      {
        id: "login-logs",
        label: "Login Logs",
        path: "/audit/login-logs",
      },
      {
        id: "user-sessions",
        label: "User Sessions",
        path: "/audit/sessions",
      },
      {
        id: "failed-login-attempts",
        label: "Failed Login Attempts",
        path: "/audit/failed-logins",
      },
      {
        id: "locked-accounts",
        label: "Locked Accounts",
        path: "/audit/locked-accounts",
      },
      {
        id: "security-reports",
        label: "Security Reports",
        path: "/audit/security-reports",
      },
      {
        id: "api-logs",
        label: "API Logs",
        path: "/audit/api-logs",
      },
      {
        id: "activity-timeline",
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
        id: "announcements",
        label: "Announcements",
        path: "/notifications/announcements",
      },
      {
        id: "email-broadcast",
        label: "Email Broadcast",
        path: "/notifications/email",
      },
      {
        id: "sms-notifications",
        label: "SMS Notifications",
        path: "/notifications/sms",
      },
      {
        id: "subscription-alerts",
        label: "Subscription Alerts",
        path: "/notifications/subscription-alerts",
      },
      {
        id: "system-notifications",
        label: "System Notifications",
        path: "/notifications/system",
      },
      {
        id: "notification-templates",
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
        id: "retailer-report",
        label: "Retailer Report",
        path: "/reports/retailers",
      },
      {
        id: "subscription-report",
        label: "Subscription Report",
        path: "/reports/subscriptions",
      },
      {
        id: "revenue-report",
        label: "Revenue Report",
        path: "/reports/revenue",
      },
      {
        id: "payment-report",
        label: "Payment Report",
        path: "/reports/payments",
      },
      {
        id: "user-report",
        label: "User Report",
        path: "/reports/users",
      },
      {
        id: "audit-report",
        label: "Audit Report",
        path: "/reports/audit",
      },
      {
        id: "backup-report",
        label: "Backup Report",
        path: "/reports/backups",
      },
      {
        id: "system-report",
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
        id: "platform-settings",
        label: "Platform Settings",
        path: "/settings/platform",
      },
      {
        id: "smtp-settings",
        label: "SMTP Settings",
        path: "/settings/smtp",
      },
      {
        id: "sms-settings",
        label: "SMS Settings",
        path: "/settings/sms",
      },
      {
        id: "backup-settings",
        label: "Backup Settings",
        path: "/settings/backup",
      },
      {
        id: "storage-settings",
        label: "Storage Settings",
        path: "/settings/storage",
      },
      {
        id: "api-settings",
        label: "API Settings",
        path: "/settings/api",
      },
      {
        id: "maintenance-mode",
        label: "Maintenance Mode",
        path: "/settings/maintenance",
      },
      {
        id: "system-configuration",
        label: "System Configuration",
        path: "/settings/configuration",
      },
      {
        id: "license-management",
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
        id: "activity-log",
        label: "Activity Log",
        path: "/account/activity",
      },
      {
        id: "notification-settings",
        label: "Notification Settings",
        path: "/account/notifications",
      },
      {
        id: "logout",
        label: "Logout",
        path: "/logout",
      },
    ],
  },
];

export default platformOwnerSidebar;
