import { colors } from "./colors";

export const spinner = {
  color: colors.primary,
  thickness: "4px",
  speed: "0.65s",
  emptyColor: "gray.200",
};

export const loaderContainer = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};

export const fullScreenLoader = {
  position: "fixed",
  inset: 0,
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  bg: "rgba(255,255,255,.75)",
  backdropFilter: "blur(2px)",
  zIndex: 9999,
};

export default {
  spinner,
  loaderContainer,
  fullScreenLoader,
};