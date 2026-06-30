import Login from "../pages/Auth/Login";
import VerifyOTP from "../pages/Auth/VerifyOTP";
import Dashboard from "../pages/Dashboard/Dashboard";

import { ROLES } from "./roles";

export const routesConfig = [

  {
    path: "/login",
    component: Login,
    public: true,
  },

  {
    path: "/verify-otp",
    component: VerifyOTP,
    public: true,
  },

  {
    path: "/dashboard",
    component: Dashboard,
    roles: [
      ROLES.SUPER_ADMIN,
      ROLES.ADMIN,
      ROLES.STORE_MANAGER,
      ROLES.PHARMACIST,
      ROLES.CASHIER,
      ROLES.STAFF,
    ],
  },
];