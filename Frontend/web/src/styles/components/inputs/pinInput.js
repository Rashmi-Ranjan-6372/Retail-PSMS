import { colors } from "../colors";

const pinInput = {
  w: "55px",
  h: "60px",
  textAlign: "center",
  fontSize: "26px",
  fontWeight: "700",
  bg: colors.white,
  border: `1.5px solid ${colors.border}`,
  borderRadius: "10px",
  transition: ".25s",

  _hover: {
    borderColor: colors.primaryLight,
  },

  _focusVisible: {
    borderColor: colors.primary,
    boxShadow: "0 0 0 4px rgba(37,99,235,.15)",
    transform: "scale(1.08)",
  },
};

export default pinInput;