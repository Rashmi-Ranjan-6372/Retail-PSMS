import { colors } from "../../common/colors";

export const pageHeader = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  flexWrap: "wrap",
  gap: "16px",
  mb: "24px",
};

export const pageTitle = {
  fontSize: "28px",
  fontWeight: "700",
  color: colors.textPrimary,
};

export const pageSubtitle = {
  mt: "4px",
  fontSize: "14px",
  color: colors.textSecondary,
};

export const pageHeaderActions = {
  display: "flex",
  alignItems: "center",
  gap: "12px",
  flexWrap: "wrap",
};

export default {
  pageHeader,
  pageTitle,
  pageSubtitle,
  pageHeaderActions,
};