import { colors } from "../common/colors";

export const modalLoader = {
  position: "absolute",
  inset: 0,
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  bg: "rgba(255,255,255,.8)",
  backdropFilter: "blur(3px)",
  borderRadius: "16px",
  zIndex: 100,
};

export default modalLoader;