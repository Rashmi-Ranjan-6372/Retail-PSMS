// src/styles/components/loaders/containers.js

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

export const inlineLoader = {
  display: "inline-flex",
  justifyContent: "center",
  alignItems: "center",
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
  justifyContent: "center",
  alignItems: "center",
  gap: "10px",
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

export const sidebarLoader = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  minH: "150px",
};

export default {
  loaderContainer,
  fullScreenLoader,
  pageLoader,
  inlineLoader,
  overlayLoader,
  buttonLoader,
  centerLoader,
  sectionLoader,
  cardLoader,
  listLoader,
  sidebarLoader,
};