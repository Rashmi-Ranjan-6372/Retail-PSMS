import { colors, shadows } from "../../common/colors";
import { cardBase } from "./cardBase";

export const glassCard = {
  ...cardBase,
  position: "relative",
  zIndex: 2,
  width: "100%",
  maxW: "480px",
  p: {
    base: "28px",
    md: "40px",
  },
  bg: "rgba(255,255,255,0.82)",
  backdropFilter: "blur(24px)",
  WebkitBackdropFilter: "blur(24px)",
  border: "1px solid rgba(255,255,255,0.35)",
  borderRadius: "24px",
  boxShadow:
    "0 20px 60px rgba(15,23,42,0.15), 0 8px 20px rgba(59,130,246,0.08)",
  transition: "all .3s ease",
  _hover: {
    transform: "translateY(-4px)",
    boxShadow:
      "0 30px 70px rgba(15,23,42,0.18), 0 10px 24px rgba(59,130,246,0.12)",
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