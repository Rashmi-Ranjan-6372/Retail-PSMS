import { colors, shadows } from "../../common/colors";
import { cardBase } from "./cardBase";

export const dashboardCard = {
  ...cardBase,
  borderRadius: "16px",
  p: "24px",

  _hover: {
    transform: "translateY(-3px)",
    boxShadow: shadows.cardHover,
  },
};

export const sidebarCard = {
  ...cardBase,
  p: "18px",
};

export const tableCard = {
  ...cardBase,
  overflow: "hidden",
};

export const filterCard = {
  ...cardBase,
  p: "18px",
  mb: "20px",
};

export default {
  dashboardCard,
  sidebarCard,
  tableCard,
  filterCard,
};