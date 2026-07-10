import { colors } from "../../common/colors";

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

export default {
  skeleton,
  skeletonCircle,
};