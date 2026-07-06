import { colors } from "./colors";

export const display = {
  fontSize: { base: "40px", md: "52px" },
  fontWeight: "800",
  lineHeight: "1.1",
  color: colors.textPrimary,
};

export const heading1 = {
  fontSize: { base: "28px", md: "32px" },
  fontWeight: "700",
  color: colors.textPrimary,
  lineHeight: "1.2",
};

export const heading2 = {
  fontSize: { base: "24px", md: "28px" },
  fontWeight: "700",
  color: colors.textPrimary,
  lineHeight: "1.3",
};

export const heading3 = {
  fontSize: { base: "20px", md: "24px" },
  fontWeight: "600",
  color: colors.textPrimary,
  lineHeight: "1.3",
};

export const heading4 = {
  fontSize: "20px",
  fontWeight: "600",
  color: colors.textPrimary,
};

export const heading5 = {
  fontSize: "18px",
  fontWeight: "600",
  color: colors.textPrimary,
};

export const heading6 = {
  fontSize: "16px",
  fontWeight: "600",
  color: colors.textPrimary,
};

export const title = {
  fontSize: "20px",
  fontWeight: "600",
  color: colors.textPrimary,
};

export const sectionTitle = {
  fontSize: "18px",
  fontWeight: "700",
  color: colors.textPrimary,
  mb: "16px",
};

export const subtitle = {
  fontSize: "15px",
  fontWeight: "500",
  color: colors.textSecondary,
};

export const body = {
  fontSize: "14px",
  color: colors.textPrimary,
  lineHeight: "1.6",
};

export const bodySmall = {
  fontSize: "13px",
  color: colors.textSecondary,
  lineHeight: "1.5",
};

export const caption = {
  fontSize: "12px",
  color: colors.textMuted,
};

export const overline = {
  fontSize: "11px",
  fontWeight: "600",
  textTransform: "uppercase",
  letterSpacing: "1px",
  color: colors.textMuted,
};

export const label = {
  fontSize: "14px",
  fontWeight: "500",
  color: colors.textPrimary,
};

export const helperText = {
  fontSize: "12px",
  color: colors.textMuted,
};

export const errorText = {
  fontSize: "12px",
  fontWeight: "500",
  color: colors.danger,
};

export const successText = {
  fontSize: "12px",
  fontWeight: "500",
  color: colors.success,
};

export const warningText = {
  fontSize: "12px",
  fontWeight: "500",
  color: colors.warning,
};

export const infoText = {
  fontSize: "12px",
  fontWeight: "500",
  color: colors.info,
};

export const link = {
  color: colors.primary,
  cursor: "pointer",
  fontWeight: "500",
  transition: ".25s ease",

  _hover: {
    color: colors.primaryDark,
    textDecoration: "underline",
  },
};

export const sidebarLabel = {
  fontSize: "14px",
  fontWeight: "600",
  color: colors.textPrimary,
};

export const navbarText = {
  fontSize: "15px",
  fontWeight: "500",
  color: colors.textPrimary,
};

export const breadcrumb = {
  fontSize: "13px",
  color: colors.textSecondary,
};

export const tableHeader = {
  fontSize: "13px",
  fontWeight: "600",
  color: colors.textSecondary,
  textTransform: "uppercase",
};

export const tableCell = {
  fontSize: "14px",
  color: colors.textPrimary,
};

export const statValue = {
  fontSize: "28px",
  fontWeight: "700",
  color: colors.primary,
};

export const statLabel = {
  fontSize: "13px",
  color: colors.textMuted,
};

export const code = {
  fontFamily: "monospace",
  fontSize: "13px",
  bg: colors.backgroundLight,
  px: "6px",
  py: "2px",
  borderRadius: "4px",
};

export const whiteButtonText = {
  color: colors.white,
  fontSize: "15px",
  fontWeight: "600",
};

export const pageTitle = {
  ...heading2,
  textAlign: "center",
  mb: "5px",
};

export const pageSubtitle = {
  ...subtitle,
  textAlign: "center",
  mb: "28px",
};

export default {
  display,
  heading1,
  heading2,
  heading3,
  heading4,
  heading5,
  heading6,
  title,
  sectionTitle,
  subtitle,
  body,
  bodySmall,
  caption,
  overline,
  label,
  helperText,
  errorText,
  successText,
  warningText,
  infoText,
  link,
  sidebarLabel,
  navbarText,
  breadcrumb,
  tableHeader,
  tableCell,
  statValue,
  statLabel,
  code,
  whiteButtonText,
  pageTitle,
  pageSubtitle,
};