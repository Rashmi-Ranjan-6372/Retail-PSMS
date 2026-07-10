import { colors } from "../../common/colors";
import { buttonBase } from "./buttonBase";

export const secondaryButton = {
  ...buttonBase,
  width: "100%",
  h: "50px",
  bg: colors.white,
  color: colors.primary,
  border: `1px solid ${colors.primary}`,

  _hover: {
    bg: colors.backgroundSecondary,
  },
};

export const outlineButton = {
  ...buttonBase,
  width: "100%",
  h: "50px",
  bg: colors.transparent,
  color: colors.primary,
  border: `1px solid ${colors.primary}`,

  _hover: {
    bg: colors.backgroundSecondary,
  },
};

export const ghostButton = {
  ...buttonBase,
  bg: colors.transparent,
  color: colors.primary,

  _hover: {
    bg: colors.backgroundSecondary,
  },
};

export const ghostFullButton = {
  ...ghostButton,
  width: "100%",
  h: "48px",
  mt: "16px",
};

export default {
  secondaryButton,
  outlineButton,
  ghostButton,
  ghostFullButton,
};