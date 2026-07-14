import { authRoutes } from "./authRoutes";
import { dashboardRoutes } from "./dashboardRoutes";
import { masterRoutes } from "./masterRoutes";
import { inventoryRoutes } from "./inventoryRoutes";
import { purchaseRoutes } from "./purchaseRoutes";
import { salesRoutes } from "./salesRoutes";
import { reportRoutes } from "./reportRoutes";
import { accountRoutes } from "./accountRoutes";
import { settingsRoutes } from "./settingsRoutes";
import { platformRoutes } from "./platformRoutes";

export const routesConfig = [
  ...authRoutes,
  ...dashboardRoutes,
  ...masterRoutes,
  ...inventoryRoutes,
  ...purchaseRoutes,
  ...salesRoutes,
  ...reportRoutes,
  ...accountRoutes,
  ...settingsRoutes,
  ...platformRoutes,
];