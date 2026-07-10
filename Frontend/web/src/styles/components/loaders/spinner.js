// src/styles/components/loaders/spinner.js

import { colors } from "../../common/colors";

export const spinner = {
  color: colors.primary,
  thickness: "4px",
  speed: "0.65s",
  emptyColor: "gray.200",
};

export const dotsLoader = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  gap: "6px",
};

export default {
  spinner,
  dotsLoader,
};