import { colors } from "../colors";

const inputAction = {
  position: "absolute",
  right: "15px",
  top: "50%",
  transform: "translateY(-50%)",
  cursor: "pointer",
  color: colors.textSecondary,
  fontSize: "18px",
  transition: ".25s",

  _hover: {
    color: colors.primary,
  },
};

export default inputAction;