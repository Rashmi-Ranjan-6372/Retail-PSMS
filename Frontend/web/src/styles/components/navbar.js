import { colors, shadows, borders, gradients } from "../common/colors";
import transitions from "../common/transitions";

export const navbarWrapper = {
  position: "sticky",
  top: 0,
  zIndex: 1000,
  h: "72px",
  px: "24px",
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  bg: colors.white,
  borderBottom: borders.light,
  boxShadow: shadows.card,
};

export const searchWrapper = {
  width: "360px",
};

export const searchInput = {
  h: "44px",
  bg: colors.background,
  border: borders.light,
  borderRadius: "12px",
  fontSize: "14px",
  color: colors.textPrimary,
  transition: transitions.normal,

  _placeholder: {
    color: colors.textMuted,
  },

  _hover: {
    borderColor: colors.primaryLight,
  },

  _focusVisible: {
    bg: colors.white,
    borderColor: colors.primary,
    boxShadow: shadows.inputFocus,
  },
};

export const searchIcon = {
  color: colors.textMuted,
  fontSize: "15px",
};

export const rightSection = {
  spacing: 4,
};

export const branchWrapper = {
  minW: "220px",
};

export const branchSelect = {
  h: "44px",
  bg: colors.white,
  border: borders.light,
  borderRadius: "12px",
  fontSize: "14px",
  color: colors.textPrimary,
  transition: transitions.normal,

  _hover: {
    borderColor: colors.primary,
  },

  _focusVisible: {
    borderColor: colors.primary,
    boxShadow: shadows.inputFocus,
  },
};

export const notificationButton = {
  w: "46px",
  h: "46px",
  minW: "46px",
  borderRadius: "12px",
  bg: colors.white,
  border: borders.light,
  color: colors.textSecondary,
  transition: transitions.normal,

  _hover: {
    bg: colors.backgroundSecondary,
    color: colors.primary,
    transform: "translateY(-2px)",
    boxShadow: shadows.hover,
  },
};

export const userButton = {
  cursor: "pointer",
  px: "12px",
  py: "8px",
  borderRadius: "14px",
  transition: transitions.normal,

  _hover: {
    bg: colors.backgroundSecondary,
  },
};

export const avatar = {
  size: "sm",
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
  minW: "220px",
  border: borders.light,
  borderRadius: "14px",
  boxShadow: shadows.dropdown,
  py: "8px",
  overflow: "hidden",
};

export const menuItem = {
  fontSize: "14px",
  color: colors.textPrimary,
  py: "10px",
  px: "16px",
  transition: transitions.fast,

  _hover: {
    bg: colors.backgroundSecondary,
    color: colors.primary,
  },

  _focus: {
    bg: colors.backgroundSecondary,
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
  borderColor: colors.borderLight,
};


export const notificationWrapper = {
  position: "relative",
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
};

export const mobileMenuButton = {
  display: {
    base: "flex",
    lg: "none",
  },
  w: "44px",
  h: "44px",
  borderRadius: "12px",
  bg: colors.background,
  border: borders.light,

  _hover: {
    bg: colors.backgroundSecondary,
    color: colors.primary,
  },
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

export const profileCard = {
  p: "16px",
  bg: gradients.background,
  borderBottom: borders.light,
};

export default {
  navbarWrapper,
  searchWrapper,
  searchInput,
  searchIcon,
  rightSection,
  branchWrapper,
  branchSelect,
  notificationButton,
  notificationWrapper,
  userButton,
  avatar,
  userInfo,
  userName,
  userRole,
  menuList,
  menuItem,
  logoutItem,
  divider,
  mobileMenuButton,
  logoWrapper,
  logoImage,
  title,
  profileCard,
};