// styles/components/layout/navbar.js

import { colors, shadows, borders } from "../../common/colors";
import transitions from "../../common/transitions";

export const navbarWrapper = {
  position: "sticky",
  top: 0,
  zIndex: 1000,
  h: "72px",
  px: "24px",
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  bg: colors.glassMedium,
  backdropFilter: "blur(24px)",
  WebkitBackdropFilter: "blur(24px)",
  borderBottom: borders.glass,
  boxShadow: shadows.glass,
};

export const searchWrapper = {
  width: "360px",
};

export const rightSection = {
  spacing: 4,
};

export const branchWrapper = {
  minW: "220px",
};

export const notificationWrapper = {
  position: "relative",
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
};

export const userButton = {
  cursor: "pointer",
  px: "12px",
  py: "8px",
  borderRadius: "14px",
  transition: transitions.normal,

  _hover: {
    bg: colors.glassHover,
    backdropFilter: "blur(16px)",
    WebkitBackdropFilter: "blur(16px)",
    boxShadow: shadows.glass,
  },
};

export const userInfo = {
  display: "flex",
  flexDirection: "column",
  alignItems: "flex-start",
  lineHeight: 1.2,
};

export const userName = {
  fontSize: "14px",
  fontWeight: "600",
  color: colors.textPrimary,
};

export const userRole = {
  fontSize: "12px",
  color: colors.textMuted,
};

export const menuList = {
  minW: "240px",
  bg: colors.glass,
  backdropFilter: "blur(24px)",
  WebkitBackdropFilter: "blur(24px)",
  border: borders.glass,
  borderRadius: "18px",
  boxShadow: shadows.glass,
  py: "8px",
  overflow: "hidden",
};

export const menuItem = {
  fontSize: "14px",
  color: colors.textPrimary,
  py: "10px",
  px: "16px",
  transition: transitions.normal,

  _hover: {
    bg: colors.glassHover,
    color: colors.primary,
  },

  _focus: {
    bg: colors.glassHover,
  },
};

export const logoutItem = {
  ...menuItem,
  color: colors.danger,

  _hover: {
    bg: colors.dangerBg,
    color: colors.dangerDark,
  },
};

export const divider = {
  borderColor: colors.glassBorder,
};

export const logoWrapper = {
  display: "flex",
  alignItems: "center",
  gap: "12px",
};

export const logoImage = {
  h: "42px",
  objectFit: "contain",
};

export const title = {
  fontSize: "18px",
  fontWeight: "700",
  color: colors.textPrimary,
};

export default {
  navbarWrapper,
  searchWrapper,
  rightSection,
  branchWrapper,
  notificationWrapper,
  userButton,
  userInfo,
  userName,
  userRole,
  menuList,
  menuItem,
  logoutItem,
  divider,
  logoWrapper,
  logoImage,
  title,
};