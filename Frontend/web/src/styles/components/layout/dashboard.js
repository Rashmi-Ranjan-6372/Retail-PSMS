import { colors } from "../../common/colors";

export const dashboardWrapper = {
  w: "100%",
  minH: "100%",
  p: 6,
};

export const dashboardHeader = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  flexWrap: "wrap",
  gap: "16px",
  mb: 8,
};

export const dashboardTitle = {
  fontSize: "28px",
  fontWeight: "700",
  color: colors.textPrimary,
};

export const dashboardSubtitle = {
  mt: 1,
  fontSize: "14px",
  color: colors.textSecondary,
};

export const dashboardActions = {
  display: "flex",
  alignItems: "center",
  gap: "12px",
  flexWrap: "wrap",
};

export default {
  dashboardWrapper,
  dashboardHeader,
  dashboardTitle,
  dashboardSubtitle,
  dashboardActions,
};