import { colors } from "../colors";

const selectInput = {
  bg: colors.white,
  border: `1.5px solid ${colors.border}`,
  borderRadius: "8px",
  fontSize: "15px",
  transition: ".25s",

  _hover: {
    borderColor: colors.primaryLight,
  },

  _focusVisible: {
    borderColor: colors.primary,
    boxShadow: "0 0 0 4px rgba(37,99,235,.15)",
  },
};

export default selectInput;