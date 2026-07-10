import { colors } from "../../common/colors";
import { buttonBase } from "./buttonBase";

export const iconButton = {
  ...buttonBase,
  w: "42px",
  h: "42px",
  minW: "42px",
  p: 0,
  bg: colors.white,
  border: `1px solid ${colors.borderLight}`,

  _hover: {
    bg: colors.backgroundSecondary,
    borderColor: colors.primary,
  },
};

export const tableActionButton = {
  ...buttonBase,
  w: "34px",
  h: "34px",
  minW: "34px",
  p: 0,
  bg: colors.backgroundLight,
  border: `1px solid ${colors.borderLight}`,

  _hover: {
    bg: colors.backgroundSecondary,
    borderColor: colors.primary,
  },
};

export default {
  iconButton,
  tableActionButton,
};