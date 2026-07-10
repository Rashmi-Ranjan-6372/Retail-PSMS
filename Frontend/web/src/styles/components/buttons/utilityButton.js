import { colors } from "../../common/colors";
import { buttonBase } from "./buttonBase";

export const smallButton = {
  ...buttonBase,
  h: "36px",
  px: "14px",
  fontSize: "13px",
};

export const largeButton = {
  ...buttonBase,
  h: "56px",
  px: "28px",
  fontSize: "16px",
};

export const linkButton = {
  ...buttonBase,
  bg: "none",
  p: 0,
  h: "auto",
  color: colors.primary,

  _hover: {
    textDecoration: "underline",
    color: colors.primaryDark,
  },
};

export default {
  smallButton,
  largeButton,
  linkButton,
};