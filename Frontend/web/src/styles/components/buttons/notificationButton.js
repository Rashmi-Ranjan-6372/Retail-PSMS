import { colors } from "../../common/colors";

export const notificationButton = {
  position: "relative",
  borderRadius: "50%",
  width: "40px",
  height: "40px",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  bg: colors.white,
  border: `1px solid ${colors.border}`,
  cursor: "pointer",
  transition: "0.2s",

  _hover: {
    bg: colors.gray100,
  },
};

export default notificationButton;