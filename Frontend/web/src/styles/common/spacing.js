// src/styles/common/spacing.js

export const spacing = {
  none: "0",

  xxs: "2px",
  xs: "4px",
  sm: "8px",
  md: "12px",
  lg: "16px",
  xl: "24px",
  xxl: "32px",
  xxxl: "48px",
  xxxxl: "64px",
  xxxxxl: "80px",

  huge: "96px",
  massive: "120px",

  auto: "auto",
};

export const radius = {
  none: "0",

  xs: "2px",
  sm: "4px",
  md: "8px",
  lg: "12px",
  xl: "16px",
  xxl: "20px",

  round: "9999px",
  full: "50%",
};

export const sizes = {
  xs: "24px",
  sm: "32px",
  md: "40px",
  lg: "48px",
  xl: "56px",
  xxl: "64px",
};

export const gaps = {
  xs: "4px",
  sm: "8px",
  md: "12px",
  lg: "16px",
  xl: "24px",
  xxl: "32px",
};

export const zIndex = {
  hide: -1,
  base: 0,

  dropdown: 1000,
  sticky: 1100,
  fixed: 1200,
  overlay: 1300,
  modal: 1400,
  popover: 1500,
  tooltip: 1600,
  toast: 1700,

  loader: 9999,
};

export default {
  spacing,
  radius,
  sizes,
  gaps,
  zIndex,
};