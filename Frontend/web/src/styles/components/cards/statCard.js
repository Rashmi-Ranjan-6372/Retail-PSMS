import { colors, shadows, borders } from "../../common/colors";
import transitions from "../../common/transitions";

export const statCard = {
  bg: colors.white,
  border: borders.light,
  borderRadius: "16px",
  boxShadow: shadows.card,
  p: 6,
  transition: transitions.normal,

  _hover: {
    transform: "translateY(-4px)",
    boxShadow: shadows.hover,
  },
};

export const statTitle = {
  fontSize: "14px",
  color: colors.textSecondary,
};

export const statValue = {
  fontSize: "28px",
  fontWeight: "700",
  color: colors.textPrimary,
};

export default {
  statCard,
  statTitle,
  statValue,
};