import { colors, shadows } from "../../common/colors";
import transitions from "../../common/transitions";

export const cardBase = {
  bg: colors.white,
  borderRadius: "12px",
  border: `1px solid ${colors.borderLight}`,
  boxShadow: shadows.card,
  transition: transitions.normal,
};

export const smallCard = {
  ...cardBase,
  p: "20px",

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

export default {
  cardBase,
  smallCard,
  clickableCard,
};