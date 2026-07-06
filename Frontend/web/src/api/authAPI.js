import api from "./api";
import { ENDPOINTS } from "./endpoints";

export const loginUser = (data) => {
  return api.post(ENDPOINTS.LOGIN, data);
};

export const verifyOTP = (data) => {
  return api.post(ENDPOINTS.VERIFY_OTP, data);
};

export const resendOTP = (data) => {
  return api.post(ENDPOINTS.RESEND_OTP, data);
};

//  Forgot Password

export const forgotPassword = (data) => {
  return api.post(ENDPOINTS.FORGOT_PASSWORD, data);
};

export const validateResetToken = (uid, token) => {
  return api.get(ENDPOINTS.VALIDATE_RESET_TOKEN(uid, token));
};

export const resetPassword = (data) => {
  return api.post(ENDPOINTS.RESET_PASSWORD, data);
};