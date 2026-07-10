import { colors } from "../../common/colors";
import { badge } from "./badge";

export const successBadge = {
  ...badge,
  bg: colors.successBg,
  color: colors.success,
};

export const dangerBadge = {
  ...badge,
  bg: colors.dangerBg,
  color: colors.danger,
};

export const warningBadge = {
  ...badge,
  bg: colors.warningBg,
  color: colors.warning,
};

export const infoBadge = {
  ...badge,
  bg: colors.infoBg,
  color: colors.info,
};

export const activeBadge = {
  ...successBadge,
};

export const inactiveBadge = {
  ...badge,
  bg: colors.borderLight,
  color: colors.textMuted,
};

export default {
  successBadge,
  dangerBadge,
  warningBadge,
  infoBadge,
  activeBadge,
  inactiveBadge,
};