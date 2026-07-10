import { colors, shadows, borders } from "../../common/colors";
import transitions from "../../common/transitions";
import { logoFloat } from "../../common/animations";

export const sidebarContainer = {
  display: "flex",
  flexDirection: "column",
  width: "290px",
  height: "100vh",

  bg: colors.glassLight,
  backdropFilter: "blur(22px)",
  WebkitBackdropFilter: "blur(22px)",

  borderRight: borders.glass,
  boxShadow: shadows.glass,
};

export const sidebarWrapper = {
  ...sidebarContainer,
  position: "sticky",
  top: 0,
  zIndex: 100,
  overflowX: "visible",
  overflowY: "hidden",
};

export const sidebarHeader = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  minH: "110px",

  bg: colors.glassHeader,
  backdropFilter: "blur(20px)",
  WebkitBackdropFilter: "blur(20px)",

  borderBottom: borders.glass,
  flexShrink: 0,
};

export const sidebarLogoWrapper = {
  width: "84px",
  height: "84px",
  borderRadius: "50%",
  bg: colors.glassStrong,
  border: borders.primary,

  display: "flex",
  justifyContent: "center",
  alignItems: "center",

  overflow: "hidden",

  backdropFilter: "blur(18px)",
  WebkitBackdropFilter: "blur(18px)",

  boxShadow: shadows.primary,
  transition: transitions.normal,
  animation: `${logoFloat} 4s ease-in-out infinite`,

  _hover: {
    transform: "scale(1.08)",
    boxShadow: shadows.primaryHover,
  },
};

export const sidebarLogoImage = {
  width: "50px",
  height: "50px",
  objectFit: "contain",
};

export const sidebarMenuWrapper = {
  flex: 1,
  overflowY: "auto",
  overflowX: "visible",
  py: 5,

  "&::-webkit-scrollbar": {
    width: "6px",
  },

  "&::-webkit-scrollbar-track": {
    background: "transparent",
  },

  "&::-webkit-scrollbar-thumb": {
    background: colors.gray300,
    borderRadius: "20px",
  },

  "&::-webkit-scrollbar-thumb:hover": {
    background: colors.gray400,
  },

  scrollbarWidth: "thin",
  scrollbarColor: `${colors.gray300} transparent`,
};

export const sidebarMenu = {
  display: "flex",
  flexDirection: "column",
  gap: "4px",
};

export const sidebarItem = {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  width: "100%",
  h: "52px",
  pl: "18px",
  pr: "18px",
  borderRadius: "16px",
  cursor: "pointer",
  userSelect: "none",
  position: "relative",
  transition: transitions.normal,

  _hover: {
    bg: colors.glassHover,
    backdropFilter: "blur(14px)",
    WebkitBackdropFilter: "blur(14px)",
    transform: "translateX(6px)",
  },
};

export const sidebarItemContent = {
  display: "flex",
  alignItems: "center",
  gap: "14px",
  flex: 1,
};

export const sidebarItemText = {
  fontSize: "14px",
  fontWeight: "600",
  color: colors.textPrimary,
  whiteSpace: "nowrap",
};

export const sidebarIcon = {
  boxSize: 5,
  fontSize: "18px",
  color: colors.primary,
  flexShrink: 0,
  transition: transitions.normal,
};

export const sidebarHover = {
  bg: colors.glassHover,
  backdropFilter: "blur(14px)",
  WebkitBackdropFilter: "blur(14px)",
};

export const sidebarActive = {
  bg: colors.primary,
  color: colors.white,
  borderRadius: "14px",
  marginX: "10px",
  boxShadow: shadows.primary,
  transform: "translateX(4px)",
  backdropFilter: "blur(18px)",
  WebkitBackdropFilter: "blur(18px)",
  transition: transitions.menu,
  zIndex: 20,

  _hover: {
    bg: colors.primary,
    color: colors.white,
    transform: "translateX(4px)",
    boxShadow: shadows.primary,
  },
};

export const sidebarInactive = {
  bg: "transparent",
  color: colors.textPrimary,
};

export const sidebarSubMenu = {
  mt: "6px",
  ml: "20px",
  pl: "14px",
  borderLeft: `2px solid ${colors.primaryTransparent}`,
};

export const sidebarChevron = {
  fontSize: "12px",
  color: colors.textSecondary,
  flexShrink: 0,
  transition: transitions.normal,
};

export default {
  sidebarContainer,
  sidebarWrapper,
  sidebarHeader,
  sidebarLogoWrapper,
  sidebarLogoImage,
  sidebarMenuWrapper,
  sidebarMenu,
  sidebarItem,
  sidebarItemContent,
  sidebarItemText,
  sidebarIcon,
  sidebarHover,
  sidebarActive,
  sidebarInactive,
  sidebarSubMenu,
  sidebarChevron,
};