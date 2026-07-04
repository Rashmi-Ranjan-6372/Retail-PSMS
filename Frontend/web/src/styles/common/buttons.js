import { colors } from "./colors";

export const primaryButton = {
  width: "100%",
  h: "50px",
  borderRadius: "8px",
  bg: colors.primary,
  color: colors.white,
  fontSize: "15px",
  fontWeight: "600",
  transition: ".25s",
  boxShadow: "0 6px 18px rgba(37,99,235,.25)",
  _hover: {
    bg: colors.primaryDark,
    transform: "translateY(-2px)",
    boxShadow: "0 10px 24px rgba(37,99,235,.35)",
  },
  _active: {
    transform: "scale(.98)",
  },
  _disabled: {
    opacity: 0.6,
    cursor: "not-allowed",
  },
};

export const secondaryButton = {
  width: "100%",
  h: "50px",
  borderRadius: "8px",
  bg: colors.white,
  color: colors.primary,
  border: `1px solid ${colors.primary}`,
  fontSize: "15px",
  fontWeight: "600",
  transition: ".25s",
  _hover: {
    bg: colors.primaryBg,
  },
};

export const dangerButton = {
  width: "100%",
  h: "50px",
  borderRadius: "8px",
  bg: colors.danger,
  color: colors.white,
  fontWeight: "600",
  transition: ".25s",
  _hover: {
    opacity: 0.9,
  },
};

export const ghostButton = {
  bg: "transparent",
  color: colors.primary,
  _hover: {
    bg: colors.primaryBg,
  },
};

export default {
  primaryButton,
  secondaryButton,
  dangerButton,
  ghostButton,
};