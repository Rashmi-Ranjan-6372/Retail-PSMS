import { colors } from "../../common/colors";

export const badge = {
  px: "10px",
  py: "4px",
  borderRadius: "999px",
  fontSize: "12px",
  fontWeight: "600",
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
};

export const primaryBadge = {
  ...badge,
  bg: colors.primary,
  color: colors.white,
};

export const secondaryBadge = {
  ...badge,
  bg: colors.secondary,
  color: colors.white,
};

export const lightBadge = {
  ...badge,
  bg: colors.backgroundLight,
  color: colors.textSecondary,
};

export const darkBadge = {
  ...badge,
  bg: colors.textPrimary,
  color: colors.white,
};

export const smallBadge = {
  ...badge,
  fontSize: "11px",
  px: "8px",
  py: "2px",
};

export const largeBadge = {
  ...badge,
  fontSize: "14px",
  px: "14px",
  py: "6px",
};

export default {
  badge,
  primaryBadge,
  secondaryBadge,
  lightBadge,
  darkBadge,
  smallBadge,
  largeBadge,
};