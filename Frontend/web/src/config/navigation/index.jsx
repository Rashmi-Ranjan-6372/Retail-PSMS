import { ROLES } from "../roles";

import adminSidebar from "./adminSidebar";
import cashierSidebar from "./cashierSidebar";
import pharmacistSidebar from "./pharmacistSidebar";
import platformOwnerSidebar from "./platformOwnerSidebar";
import staffSidebar from "./staffSidebar";
import storeManagerSidebar from "./storeManagerSidebar";
import superAdminSidebar from "./superAdminSidebar";

const sidebarMap = {
  [ROLES.ADMIN]: adminSidebar,
  [ROLES.CASHIER]: cashierSidebar,
  [ROLES.PHARMACIST]: pharmacistSidebar,
  [ROLES.PLATFORM_OWNER]: platformOwnerSidebar,
  [ROLES.STAFF]: staffSidebar,
  [ROLES.STORE_MANAGER]: storeManagerSidebar,
  [ROLES.SUPER_ADMIN]: superAdminSidebar,
};

export const getSidebarByRole = (role) => sidebarMap[role] || [];