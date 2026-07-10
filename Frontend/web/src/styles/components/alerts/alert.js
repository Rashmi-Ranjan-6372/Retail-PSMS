import { colors } from "./colors";

export const alertContainer = {
  borderRadius: "8px",
  p: "12px",
  mb: "18px",
  fontSize: "14px",
};

export const successAlert = {
  ...alertContainer,
  bg: colors.successBg,
  color: colors.success,
  border: `1px solid ${colors.success}`,
};

export const errorAlert = {
  ...alertContainer,
  bg: colors.dangerBg,
  color: colors.danger,
  border: `1px solid ${colors.danger}`,
};

export const warningAlert = {
  ...alertContainer,
  bg: colors.warningBg,
  color: colors.warning,
  border: `1px solid ${colors.warning}`,
};

export const infoAlert = {
  ...alertContainer,
  bg: colors.infoBg,
  color: colors.info,
  border: `1px solid ${colors.info}`,
};


export const alertTitle = {
  fontWeight: "600",
  fontSize: "15px",
  mb: "4px",
};

export const alertDescription = {
  fontSize: "14px",
  lineHeight: "1.6",
};

export const alertIcon = {
  mr: "10px",
  fontSize: "18px",
};

export default {
  alertContainer,
  successAlert,
  errorAlert,
  warningAlert,
  infoAlert,
  alertTitle,
  alertDescription,
  alertIcon,
};