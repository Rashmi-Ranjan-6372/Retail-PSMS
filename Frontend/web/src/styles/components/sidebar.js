import { colors, shadows, borders, gradients } from "../common/colors";
import transitions from "../common/transitions";
import { logoFloat } from "../common/animations";

export const sidebarContainer = {
    display: "flex",
    flexDirection: "column",
    width: "290px",
    height: "100vh",
    bg: colors.white,
    borderRight: "none",
    boxShadow: "none",
};

export const sidebarWrapper = {
    ...sidebarContainer,
    position: "sticky",
    top: 0,
    height: "100vh",
    overflowX: "visible",
    overflowY: "hidden",
};

export const sidebarHeader = {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    minH: "110px",
    bg: gradients.background,
    borderBottom: borders.light,
    flexShrink: 0,
};

export const sidebarLogoWrapper = {
    width: "84px",
    height: "84px",
    borderRadius: "50%",
    bg: colors.white,
    border: borders.primary,
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    overflow: "hidden",
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
    pl: 0,
    pr: 0,
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
    overflow: "visible",
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
        bg: colors.backgroundSecondary,
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
    transition: transitions.fast,
};

export const sidebarHover = {
    bg: colors.backgroundSecondary,
};

export const sidebarActive = {
    bg: colors.backgroundLight,
    color: colors.textPrimary,
    borderRadius: "16px 0 0 16px",
    marginRight: "-16px",
    paddingRight: "34px",
    transform: "translateX(6px)",
    boxShadow: "none",
    zIndex: 20,
};

export const sidebarInactive = {
    bg: colors.transparent,
    color: colors.textPrimary,
};

export const sidebarSubMenu = {
    mt: "6px",
    ml: "20px",
    pl: "14px",
    borderLeft: `2px solid ${colors.gray200}`,
};

export const sidebarChevron = {
    fontSize: "12px",
    color: colors.textSecondary,
    flexShrink: 0,
    transition: transitions.fast,
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