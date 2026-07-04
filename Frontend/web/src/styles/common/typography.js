import { colors } from "./colors";

export const heading1 = {
  fontSize: "32px",
  fontWeight: "700",
  color: colors.textPrimary,
};

export const heading2 = {
  fontSize: "28px",
  fontWeight: "700",
  color: colors.textPrimary,
};

export const heading3 = {
  fontSize: "24px",
  fontWeight: "600",
  color: colors.textPrimary,
};

export const title = {
  fontSize: "20px",
  fontWeight: "600",
  color: colors.textPrimary,
};

export const subtitle = {
  fontSize: "15px",
  color: colors.textSecondary,
};

export const body = {
  fontSize: "14px",
  color: colors.textPrimary,
};

export const caption = {
  fontSize: "12px",
  color: colors.textMuted,
};

export const link = {
  color: colors.primary,
  cursor: "pointer",
  fontWeight: "500",
  _hover: {
    textDecoration: "underline",
  },
};

export default {
  heading1,
  heading2,
  heading3,
  title,
  subtitle,
  body,
  caption,
  link,
};