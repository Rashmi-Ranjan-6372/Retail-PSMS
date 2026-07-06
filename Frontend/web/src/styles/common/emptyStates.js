import { colors, shadows } from "./colors";
import transitions from "./transitions";

export const emptyState = {
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  justifyContent: "center",
  py: "60px",
  px: "24px",
  textAlign: "center",
  color: colors.textMuted,
};

export const emptyStateCard = {
  bg: colors.white,
  border: `1px dashed ${colors.border}`,
  borderRadius: "16px",
  p: "40px",
  boxShadow: shadows.card,
  transition: transitions.normal,
  textAlign: "center",

  _hover: {
    boxShadow: shadows.cardHover,
  },
};

export const emptyStateIcon = {
  boxSize: 16,
  color: colors.primary,
  opacity: 0.7,
  mb: "20px",
};

export const emptyStateTitle = {
  fontSize: "20px",
  fontWeight: "600",
  color: colors.textPrimary,
  mb: "8px",
};

export const emptyStateDescription = {
  fontSize: "14px",
  color: colors.textSecondary,
  maxW: "420px",
  lineHeight: "1.6",
  mb: "24px",
};

export const emptyStateActions = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  gap: "12px",
  flexWrap: "wrap",
};

export default {
  emptyState,
  emptyStateCard,
  emptyStateIcon,
  emptyStateTitle,
  emptyStateDescription,
  emptyStateActions,
};