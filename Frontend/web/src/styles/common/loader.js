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

export const pageLoader = {
  minH: "70vh",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};

export const tableLoader = {
  py: "40px",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};

export const inlineLoader = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
};

export const overlayLoader = {
  position: "absolute",
  inset: 0,
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  bg: "rgba(255,255,255,.6)",
  backdropFilter: "blur(1px)",
  zIndex: 10,
};

export const buttonLoader = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  gap: "10px",
};

export const cardLoader = {
  display: "flex",
  flexDirection: "column",
  gap: "16px",
  p: "20px",
};

export const listLoader = {
  display: "flex",
  flexDirection: "column",
  gap: "12px",
};

export const skeleton = {
  borderRadius: "8px",
  startColor: colors.backgroundLight,
  endColor: colors.backgroundSecondary,
  fadeDuration: 0.4,
  speed: 0.8,
};

export const skeletonCircle = {
  borderRadius: "50%",
  startColor: colors.backgroundLight,
  endColor: colors.backgroundSecondary,
};

export const progressLoader = {
  size: "sm",
  colorScheme: "blue",
  borderRadius: "999px",
};

export const dotsLoader = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  gap: "6px",
};

export const loaderText = {
  mt: "12px",
  color: colors.textSecondary,
  fontSize: "14px",
  fontWeight: "500",
};

export const centerLoader = {
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
  gap: "12px",
};

export const sectionLoader = {
  minH: "250px",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};

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

export const sidebarLoader = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  minH: "150px",
};

export const dashboardLoader = {
  display: "grid",
  gridTemplateColumns: {
    base: "1fr",
    md: "repeat(2,1fr)",
    xl: "repeat(4,1fr)",
  },
  gap: "20px",
};

export const tableSkeleton = {
  display: "flex",
  flexDirection: "column",
  gap: "10px",
  py: "20px",
};

export const imageLoader = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  bg: colors.backgroundLight,
  borderRadius: "12px",
};

export default {
  spinner,
  loaderContainer,
  fullScreenLoader,
  pageLoader,
  tableLoader,
  inlineLoader,
  buttonLoader,
  overlayLoader,
  cardLoader,
  listLoader,
  skeleton,
  skeletonCircle,
  progressLoader,
  dotsLoader,
  loaderText,
  centerLoader,
  sectionLoader,
  modalLoader,
  sidebarLoader,
  dashboardLoader,
  tableSkeleton,
  imageLoader,
};