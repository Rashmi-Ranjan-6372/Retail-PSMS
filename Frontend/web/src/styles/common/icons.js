// src/styles/common/icons.js

import { colors, shadows } from "./colors";
import { spin } from "./animations";
import transitions from "./transitions";

export const icon = {
  boxSize: 5,
  color: colors.textSecondary,
  transition: transitions.icon,
};

export const iconSmall = {
  ...icon,
  boxSize: 4,
};

export const iconMedium = {
  ...icon,
  boxSize: 5,
};

export const iconLarge = {
  ...icon,
  boxSize: 6,
};

export const iconXLarge = {
  ...icon,
  boxSize: 8,
};

export const iconContainer = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  w: "36px",
  h: "36px",
  borderRadius: "8px",
};

export const circleIconContainer = {
  ...iconContainer,
  borderRadius: "50%",
};

export const roundedIconContainer = {
  ...iconContainer,
  borderRadius: "12px",
};

export const squareIconContainer = {
  ...iconContainer,
  borderRadius: "4px",
};

export const filledIcon = {
  ...iconContainer,
  bg: colors.primary,
  color: colors.white,
};

export const successFilledIcon = {
  ...iconContainer,
  bg: colors.success,
  color: colors.white,
};

export const dangerFilledIcon = {
  ...iconContainer,
  bg: colors.danger,
  color: colors.white,
};

export const warningFilledIcon = {
  ...iconContainer,
  bg: colors.warning,
  color: colors.white,
};

export const infoFilledIcon = {
  ...iconContainer,
  bg: colors.info,
  color: colors.white,
};

export const outlinedIcon = {
  ...iconContainer,
  bg: colors.white,
  border: `1px solid ${colors.borderLight}`,
};

export const clickableIcon = {
  ...icon,
  cursor: "pointer",
  borderRadius: "6px",
  p: "4px",

  _hover: {
    bg: colors.backgroundSecondary,
    color: colors.primary,
    transform: "scale(1.08)",
  },

  _active: {
    transform: "scale(.95)",
  },
};

export const clickableIconSmall = {
  ...clickableIcon,
  p: "2px",
};

export const clickableIconLarge = {
  ...clickableIcon,
  p: "8px",
};

export const iconButton = {
  ...iconContainer,
  cursor: "pointer",
  transition: transitions.button,

  _hover: {
    bg: colors.backgroundSecondary,
    color: colors.primary,
    transform: "translateY(-2px)",
    boxShadow: shadows.hover,
  },

  _active: {
    transform: "scale(.96)",
  },
};

export const sidebarIcon = {
  boxSize: 5,
  color: colors.primary,
};

export const navbarIcon = {
  boxSize: 5,
  color: colors.textSecondary,

  _hover: {
    color: colors.primary,
  },
};

export const cardIcon = {
  boxSize: 7,
  color: colors.primary,
};

export const avatarIcon = {
  boxSize: 10,
  color: colors.white,
};

export const activeIcon = {
  color: colors.primary,
};

export const hoverIcon = {
  transition: transitions.icon,

  _hover: {
    color: colors.primary,
  },
};

export const primaryIcon = {
  color: colors.primary,
};

export const secondaryIcon = {
  color: colors.secondary,
};

export const successIcon = {
  color: colors.success,
};

export const warningIcon = {
  color: colors.warning,
};

export const dangerIcon = {
  color: colors.danger,
};

export const infoIcon = {
  color: colors.info,
};

export const whiteIcon = {
  color: colors.white,
};

export const mutedIcon = {
  color: colors.textMuted,
};

export const disabledIcon = {
  color: colors.borderDark,
  opacity: 0.5,
  cursor: "not-allowed",
};

export const shadowIcon = {
  boxShadow: shadows.card,
};

export const rotatingIcon = {
  animation: `${spin} 1s linear infinite`,
};

export default {
  icon,
  iconSmall,
  iconMedium,
  iconLarge,
  iconXLarge,
  iconContainer,
  circleIconContainer,
  roundedIconContainer,
  squareIconContainer,
  filledIcon,
  successFilledIcon,
  dangerFilledIcon,
  warningFilledIcon,
  infoFilledIcon,
  outlinedIcon,
  clickableIcon,
  clickableIconSmall,
  clickableIconLarge,
  iconButton,
  sidebarIcon,
  navbarIcon,
  cardIcon,
  avatarIcon,
  activeIcon,
  hoverIcon,
  primaryIcon,
  secondaryIcon,
  successIcon,
  warningIcon,
  dangerIcon,
  infoIcon,
  whiteIcon,
  mutedIcon,
  disabledIcon,
  shadowIcon,
  rotatingIcon,
};