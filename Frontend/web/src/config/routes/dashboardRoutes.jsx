import Dashboard from "../../pages/Dashboard/Dashboard";
import { ROLES } from "../roles";

export const dashboardRoutes = [
  {
    path: "/dashboard",
    component: Dashboard,
    roles: [
      ROLES.SUPER_ADMIN,
      ROLES.PLATFORM_OWNER,
      ROLES.ADMIN,
      ROLES.STORE_MANAGER,
      ROLES.PHARMACIST,
      ROLES.CASHIER,
      ROLES.STAFF,
    ],
  },
];