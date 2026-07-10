import { colors } from "../../common/colors";
import { cardBase } from "./cardBase";

export const emptyStateCard = {
  ...cardBase,
  p: "40px",
  textAlign: "center",
  color: colors.textMuted,
};

export default {
  emptyStateCard,
};