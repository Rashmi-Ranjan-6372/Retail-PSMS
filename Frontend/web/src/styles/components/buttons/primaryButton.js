import { colors, shadows } from "../../common/colors";
import { buttonBase } from "./buttonBase";

export const primaryButton = {
  ...buttonBase,
  width: "100%",
  h: "50px",
  bg: colors.primary,
  color: colors.white,
  boxShadow: shadows.primary,

  _hover: {
    bg: colors.primaryDark,
    transform: "translateY(-2px)",
    boxShadow: shadows.primaryHover,
  },

  _active: {
    transform: "scale(.98)",
  },
};

export const successButton = {
  ...buttonBase,
  width: "100%",
  h: "50px",
  bg: colors.success,
  color: colors.white,

  _hover: {
    opacity: 0.9,
  },
};

export const warningButton = {
  ...buttonBase,
  width: "100%",
  h: "50px",
  bg: colors.warning,
  color: colors.white,

  _hover: {
    opacity: 0.9,
  },
};

export const dangerButton = {
  ...buttonBase,
  width: "100%",
  h: "50px",
  bg: colors.danger,
  color: colors.white,

  _hover: {
    opacity: 0.9,
  },
};

export default {
  primaryButton,
  successButton,
  warningButton,
  dangerButton,
};