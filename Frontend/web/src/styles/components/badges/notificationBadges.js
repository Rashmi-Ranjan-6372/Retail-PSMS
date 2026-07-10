import { colors } from "../../common/colors";

export const notificationBadge = {
  position: "absolute",
  top: "2px",
  right: "2px",
  transform: "translate(50%, -50%)",
  minW: "18px",
  h: "18px",
  px: "0",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  borderRadius: "50%",
  bg: colors.danger,
  color: colors.white,
  fontSize: "10px",
  fontWeight: "700",
  border: `2px solid ${colors.white}`,
  zIndex: 999,
  pointerEvents: "none",
};

export default {
  notificationBadge,
};