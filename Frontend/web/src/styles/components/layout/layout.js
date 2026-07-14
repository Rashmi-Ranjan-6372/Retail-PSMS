import { colors } from "../../common/colors";

export const layoutWrapper = {
  display: "flex",
  width: "100%",
  minH: "100vh",
  bg: colors.backgroundLight,
};

export const contentWrapper = {
  flex: 1,
  display: "flex",
  flexDirection: "column",
  minW: 0,
};

export const pageWrapper = {
  flex: 1,
  position: "relative",
  overflowY: "auto",
};

export const pageContent = {
  position: "relative",
  zIndex: 2,
  p: 6,
};

export default {
  layoutWrapper,
  contentWrapper,
  pageWrapper,
  pageContent,
};