import { colors, shadows } from "../../common/colors";
import { cardBase } from "./cardBase";

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

export const modalCard = {
  ...cardBase,
  p: "30px",
  borderRadius: "16px",
  boxShadow: shadows.modal,
};

export const loginCard = {
  ...glassCard,
};

export default {
  glassCard,
  modalCard,
  loginCard,
};