import transitions from "../../common/transitions";

export const buttonBase = {
  borderRadius: "8px",
  fontWeight: "600",
  fontSize: "15px",
  transition: transitions.normal,
  cursor: "pointer",

  _disabled: {
    opacity: 0.6,
    cursor: "not-allowed",
  },
};

export default {
  buttonBase,
};