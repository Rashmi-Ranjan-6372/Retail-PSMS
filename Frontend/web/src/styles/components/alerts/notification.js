import { colors } from "../../common/colors";

export const notification = {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  width: "100%",
  padding: "12px 16px",
  borderRadius: "8px",
  backgroundColor: colors.primaryLight,
  border: `1px solid ${colors.primary}`,
  color: colors.textPrimary,
  fontSize: "14px",
  fontWeight: "500",
  boxShadow: "sm",
};

export default notification;