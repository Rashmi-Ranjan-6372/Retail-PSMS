import { colors, shadows } from "./colors";
import transitions from "./transitions";

export const buttonBase = {
  borderRadius: "8px",
  fontWeight: "600",
  fontSize: "15px",
  transition: transitions.normal,
  cursor: "pointer",

  _disabled: {
    opacity: 0.6,
    cursor: "not-allowed",
  },
};

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

export const secondaryButton = {
  ...buttonBase,
  width: "100%",
  h: "50px",
  bg: colors.white,
  color: colors.primary,
  border: `1px solid ${colors.primary}`,

  _hover: {
    bg: colors.backgroundSecondary,
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

export const outlineButton = {
  ...buttonBase,
  width: "100%",
  h: "50px",
  bg: colors.transparent,
  color: colors.primary,
  border: `1px solid ${colors.primary}`,

  _hover: {
    bg: colors.backgroundSecondary,
  },
};

export const ghostButton = {
  ...buttonBase,
  bg: colors.transparent,
  color: colors.primary,

  _hover: {
    bg: colors.backgroundSecondary,
  },
};

export const ghostFullButton = {
  ...ghostButton,
  width: "100%",
  h: "48px",
  mt: "16px",
};

export const iconButton = {
  ...buttonBase,
  w: "42px",
  h: "42px",
  minW: "42px",
  p: 0,
  bg: colors.white,
  border: `1px solid ${colors.borderLight}`,

  _hover: {
    bg: colors.backgroundSecondary,
    borderColor: colors.primary,
  },
};

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

export const tableActionButton = {
  ...buttonBase,
  w: "34px",
  h: "34px",
  minW: "34px",
  p: 0,
  bg: colors.backgroundLight,
  border: `1px solid ${colors.borderLight}`,

  _hover: {
    bg: colors.backgroundSecondary,
    borderColor: colors.primary,
  },
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
  buttonBase,
  primaryButton,
  secondaryButton,
  successButton,
  warningButton,
  dangerButton,
  outlineButton,
  ghostButton,
  ghostFullButton,
  iconButton,
  smallButton,
  largeButton,
  tableActionButton,
  linkButton,
};