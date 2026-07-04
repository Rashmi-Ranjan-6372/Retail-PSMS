import { colors } from "./colors";

export const glassCard = {
  position: "relative",
  zIndex: 2,
  width: "100%",
  maxW: "450px",
  p: "32px",
  bg: colors.glass,
  backdropFilter: "blur(18px)",
  border: `1px solid ${colors.glassBorder}`,
  borderRadius: "18px",
  boxShadow:
    "0 12px 35px rgba(0,0,0,.08), 0 0 30px rgba(37,99,235,.08)",
  transition: ".3s",
  _hover: {
    transform: "translateY(-3px)",
    boxShadow:
      "0 20px 45px rgba(0,0,0,.10), 0 0 40px rgba(37,99,235,.12)",
  },
};

export const smallCard = {
  bg: colors.white,
  borderRadius: "12px",
  border: `1px solid ${colors.borderLight}`,
  p: "20px",
  boxShadow: "0 2px 8px rgba(0,0,0,.06)",
  transition: ".25s",
  _hover: {
    transform: "translateY(-2px)",
    boxShadow: "0 8px 18px rgba(0,0,0,.10)",
  },
};

export const dashboardCard = {
  bg: colors.white,
  borderRadius: "16px",
  border: `1px solid ${colors.borderLight}`,
  p: "24px",
  boxShadow: "0 4px 12px rgba(0,0,0,.06)",
  transition: ".25s",
  _hover: {
    transform: "translateY(-3px)",
    boxShadow: "0 10px 24px rgba(0,0,0,.10)",
  },
};

export const modalCard = {
  bg: colors.white,
  borderRadius: "16px",
  p: "30px",
  boxShadow: "0 20px 45px rgba(0,0,0,.18)",
  border: `1px solid ${colors.borderLight}`,
};

export const sidebarCard = {
  bg: colors.white,
  borderRadius: "12px",
  p: "18px",
  border: `1px solid ${colors.borderLight}`,
  boxShadow: "0 2px 8px rgba(0,0,0,.05)",
};

export const profileCard = {
  bg: colors.white,
  borderRadius: "20px",
  p: "30px",
  textAlign: "center",
  border: `1px solid ${colors.borderLight}`,
  boxShadow: "0 8px 20px rgba(0,0,0,.08)",
};

export default {
    glassCard,
    smallCard,
    dashboardCard,
    modalCard,
    sidebarCard,
    profileCard
};