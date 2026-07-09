import { colors, shadows, borders } from "../common/colors";
import transitions from "../common/transitions";

export const dashboardWrapper = {
  w: "100%",
  minH: "100%",
  p: 6,
};

export const dashboardHeader = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  mb: 8,
};

export const dashboardTitle = {
  fontSize: "28px",
  fontWeight: "700",
  color: colors.textPrimary,
};

export const dashboardSubtitle = {
  mt: 1,
  color: colors.textSecondary,
  fontSize: "14px",
};

export const statCard = {
  bg: colors.white,
  border: borders.light,
  borderRadius: "16px",
  boxShadow: shadows.card,
  p: 6,
  transition: transitions.normal,

  _hover: {
    transform: "translateY(-4px)",
    boxShadow: shadows.hover,
  },
};

export const statTitle = {
  fontSize: "14px",
  color: colors.textSecondary,
};

export const statValue = {
  fontSize: "28px",
  fontWeight: "700",
  color: colors.textPrimary,
};

export default {
  dashboardWrapper,
  dashboardHeader,
  dashboardTitle,
  dashboardSubtitle,
  statCard,
  statTitle,
  statValue,
};