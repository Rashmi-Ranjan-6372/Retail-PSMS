import { colors, shadows } from "./colors";
import transitions from "./transitions";

export const cardBase = {
  bg: colors.white,
  borderRadius: "12px",
  border: `1px solid ${colors.borderLight}`,
  boxShadow: shadows.card,
  transition: transitions.normal,
};

export const glassCard = {
  ...cardBase,
  position: "relative",
  zIndex: 2,
  width: "100%",
  maxW: "450px",
  p: "32px",
  bg: colors.glass,
  backdropFilter: "blur(18px)",
  border: `1px solid ${colors.glassBorder}`,
  borderRadius: "18px",
  boxShadow: shadows.glass,

  _hover: {
    transform: "translateY(-3px)",
    boxShadow: shadows.modal,
  },
};

export const smallCard = {
  ...cardBase,
  p: "20px",

  _hover: {
    transform: "translateY(-2px)",
    boxShadow: shadows.cardHover,
  },
};

export const dashboardCard = {
  ...cardBase,
  borderRadius: "16px",
  p: "24px",

  _hover: {
    transform: "translateY(-3px)",
    boxShadow: shadows.cardHover,
  },
};

export const modalCard = {
  ...cardBase,
  p: "30px",
  borderRadius: "16px",
  boxShadow: shadows.modal,
};

export const sidebarCard = {
  ...cardBase,
  p: "18px",
};

export const profileCard = {
  ...cardBase,
  p: "30px",
  borderRadius: "20px",
  textAlign: "center",
};

export const tableCard = {
  ...cardBase,
  overflow: "hidden",
};

export const statsCard = {
  ...cardBase,
  p: "20px",
  borderRadius: "14px",

  _hover: {
    transform: "translateY(-2px)",
    boxShadow: shadows.cardHover,
  },
};

export const clickableCard = {
  ...cardBase,
  p: "20px",
  cursor: "pointer",

  _hover: {
    transform: "translateY(-2px)",
    borderColor: colors.primary,
    boxShadow: shadows.primary,
  },
};

export const formCard = {
  ...cardBase,
  p: "24px",
};

export const filterCard = {
  ...cardBase,
  p: "18px",
  mb: "20px",
};

export const loginCard = {
  ...glassCard,
};

export const emptyStateCard = {
  ...cardBase,
  p: "40px",
  textAlign: "center",
  color: colors.textMuted,
};

export default {
  cardBase,
  glassCard,
  smallCard,
  dashboardCard,
  modalCard,
  sidebarCard,
  profileCard,
  tableCard,
  statsCard,
  clickableCard,
  formCard,
  filterCard,
  loginCard,
  emptyStateCard,
};