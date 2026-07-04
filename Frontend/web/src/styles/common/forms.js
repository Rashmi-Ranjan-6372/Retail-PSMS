import { colors } from "./colors";

export const form = {
  width: "100%",
};

export const formGroup = {
  position: "relative",
  mb: "24px",
};

export const textInput = {
  width: "100%",
  h: "55px",
  px: "15px",
  pt: "20px",
  pb: "0",
  bg: colors.white,
  border: `1.5px solid ${colors.border}`,
  borderRadius: "8px",
  fontSize: "15px",
  transition: ".25s",
  _hover: {
    borderColor: colors.primaryLight,
  },
  _focusVisible: {
    borderColor: colors.primary,
    boxShadow: "0 0 0 4px rgba(37,99,235,.15)",
  },
};

export const floatingLabel = {
  position: "absolute",
  left: "15px",
  top: "17px",
  bg: colors.white,
  color: colors.textMuted,
  fontSize: "14px",
  pointerEvents: "none",
  transition: ".25s",
};

export const floatingLabelActive = {
  top: "-10px",
  left: "12px",
  px: "6px",
  fontSize: "12px",
  fontWeight: "600",
  color: colors.primary,
};

export const inputAction = {
  position: "absolute",
  right: "15px",
  top: "50%",
  transform: "translateY(-50%)",
  cursor: "pointer",
  color: colors.textSecondary,
  fontSize: "18px",
  transition: ".25s",
  _hover: {
    color: colors.primary,
  },
};

export const errorAlert = {
  p: "12px",
  mb: "18px",
  bg: colors.dangerBg,
  color: colors.danger,
  border: `1px solid ${colors.danger}`,
  borderRadius: "8px",
  fontSize: "14px",
};

export const successAlert = {
  p: "12px",
  mb: "18px",
  bg: colors.successBg,
  color: colors.success,
  border: `1px solid ${colors.success}`,
  borderRadius: "8px",
  fontSize: "14px",
};

export const pinContainer = {
  display: "flex",
  justifyContent: "space-between",
  gap: "10px",
  mb: "24px",
};

export const pinInput = {
  w: "55px",
  h: "60px",
  textAlign: "center",
  fontSize: "26px",
  fontWeight: "700",
  bg: colors.white,
  border: `1.5px solid ${colors.border}`,
  borderRadius: "10px",
  transition: ".25s",
  _hover: {
    borderColor: colors.primaryLight,
  },
  _focusVisible: {
    borderColor: colors.primary,
    boxShadow: "0 0 0 4px rgba(37,99,235,.15)",
    transform: "scale(1.08)",
  },
};

export const textArea = {
  bg: colors.white,
  border: `1.5px solid ${colors.border}`,
  borderRadius: "8px",
  fontSize: "15px",
  transition: ".25s",
  _hover: {
    borderColor: colors.primaryLight,
  },
  _focusVisible: {
    borderColor: colors.primary,
    boxShadow: "0 0 0 4px rgba(37,99,235,.15)",
  },
};

export const selectInput = {
  bg: colors.white,
  border: `1.5px solid ${colors.border}`,
  borderRadius: "8px",
  fontSize: "15px",
  transition: ".25s",
  _hover: {
    borderColor: colors.primaryLight,
  },
  _focusVisible: {
    borderColor: colors.primary,
    boxShadow: "0 0 0 4px rgba(37,99,235,.15)",
  },
};

export const checkbox = {
  colorScheme: "blue",
};

export const radio = {
  colorScheme: "blue",
};

export default {
  form,
  formGroup,
  textInput,
  floatingLabel,
  floatingLabelActive,
  inputAction,
  errorAlert,
  successAlert,
  pinContainer,
  pinInput,
  textArea,
  selectInput,
  checkbox,
  radio,
};