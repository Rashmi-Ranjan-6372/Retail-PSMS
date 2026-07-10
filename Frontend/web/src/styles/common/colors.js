// src/styles/common/colors.js

export const colors = {
  // Primary
  primary: "#2563EB",
  primaryDark: "#1D4ED8",
  primaryLight: "#3B82F6",

  // Secondary
  secondary: "#0EA5E9",
  secondaryDark: "#0284C7",
  secondaryLight: "#38BDF8",

  // Success
  success: "#16A34A",
  successDark: "#15803D",
  successLight: "#22C55E",
  successBg: "#DCFCE7",

  // Danger
  danger: "#DC2626",
  dangerDark: "#B91C1C",
  dangerLight: "#EF4444",
  dangerBg: "#FEF2F2",

  // Warning
  warning: "#D97706",
  warningDark: "#B45309",
  warningLight: "#F59E0B",
  warningBg: "#FEF3C7",

  // Info
  info: "#2563EB",
  infoDark: "#1D4ED8",
  infoLight: "#60A5FA",
  infoBg: "#DBEAFE",

  // Text
  text: "#1E293B",
  textPrimary: "#1E293B",
  textSecondary: "#334155",
  textLight: "#64748B",
  textMuted: "#94A3B8",
  textWhite: "#FFFFFF",

  // Background
  background: "#F8FAFC",
  backgroundSecondary: "#EEF6FF",
  backgroundLight: "#E9EEF5",
  backgroundDark: "#E2E8F0",

  // Base Colors
  white: "#FFFFFF",
  black: "#000000",
  transparent: "transparent",

  // Borders
  border: "#CBD5E1",
  borderLight: "#E2E8F0",
  borderDark: "#94A3B8",

  // Glassmorphism
  glass: "rgba(255,255,255,0.70)",
  glassStrong: "rgba(255,255,255,0.82)",
  glassLight: "rgba(255,255,255,0.65)",
  glassMedium: "rgba(255,255,255,0.45)",
  glassDark: "rgba(255,255,255,0.35)",

  glassHover: "rgba(255,255,255,0.28)",
  glassActive: "rgba(255,255,255,0.45)",
  glassHeader: "rgba(255,255,255,0.15)",

  glassBorder: "rgba(255,255,255,0.35)",
  glassBorderStrong: "rgba(255,255,255,0.60)",

  // Overlays
  overlay: "rgba(255,255,255,.75)",
  overlayDark: "rgba(0,0,0,.45)",

  // Transparent Theme Colors
  primaryTransparent: "rgba(37,99,235,.25)",
  secondaryTransparent: "rgba(14,165,233,.25)",

  // Gray Scale
  gray50: "#F8FAFC",
  gray100: "#F1F5F9",
  gray200: "#E2E8F0",
  gray300: "#CBD5E1",
  gray400: "#94A3B8",
  gray500: "#64748B",
  gray600: "#475569",
  gray700: "#334155",
  gray800: "#1E293B",
  gray900: "#0F172A",
};

export const shadows = {
  primary: "0 6px 18px rgba(37,99,235,.25)",
  primaryHover: "0 10px 24px rgba(37,99,235,.35)",

  card: "0 4px 12px rgba(0,0,0,.06)",
  cardHover: "0 10px 24px rgba(0,0,0,.10)",

  glass: "0 12px 35px rgba(31,38,135,.12)",
  glassSoft: "0 8px 24px rgba(31,38,135,.10)",
  glassStrong: "0 18px 45px rgba(31,38,135,.18)",

  modal: "0 20px 45px rgba(0,0,0,.18)",
  sidebar: "2px 0 12px rgba(0,0,0,.06)",
  dropdown: "0 8px 24px rgba(0,0,0,.12)",

  inputFocus: "0 0 0 4px rgba(37,99,235,.15)",

  table: "0 2px 8px rgba(0,0,0,.05)",
  hover: "0 8px 20px rgba(0,0,0,.10)",

  none: "none",
};

export const borders = {
  light: `1px solid ${colors.borderLight}`,
  normal: `1px solid ${colors.border}`,
  dark: `1px solid ${colors.borderDark}`,

  primary: `1px solid ${colors.primary}`,
  success: `1px solid ${colors.success}`,
  danger: `1px solid ${colors.danger}`,
  warning: `1px solid ${colors.warning}`,
  info: `1px solid ${colors.info}`,

  glass: `1px solid ${colors.glassBorder}`,
  glassStrong: `1px solid ${colors.glassBorderStrong}`,
};

export const gradients = {
  primary:
    "linear-gradient(135deg,#2563EB 0%,#3B82F6 100%)",

  secondary:
    "linear-gradient(135deg,#0EA5E9 0%,#38BDF8 100%)",

  background:
    "linear-gradient(135deg,#F8FAFC 0%,#EEF6FF 45%,#E0F2FE 100%)",

  success:
    "linear-gradient(135deg,#16A34A,#22C55E)",

  danger:
    "linear-gradient(135deg,#DC2626,#EF4444)",
};

export default {
  colors,
  shadows,
  borders,
  gradients,
};