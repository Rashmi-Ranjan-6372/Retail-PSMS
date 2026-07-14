import { colors } from "../../common/colors";

export const toast = {
  borderRadius: "8px",
  padding: "12px 16px",
  fontSize: "14px",
  fontWeight: "500",
  color: colors.white,
  backgroundColor: colors.success,
  boxShadow: "lg",
};

export const successToast = {
  ...toast,
  backgroundColor: colors.success,
};

export const errorToast = {
  ...toast,
  backgroundColor: colors.danger,
};

export const warningToast = {
  ...toast,
  backgroundColor: colors.warning,
};

export const infoToast = {
  ...toast,
  backgroundColor: colors.info,
};

export default toast;