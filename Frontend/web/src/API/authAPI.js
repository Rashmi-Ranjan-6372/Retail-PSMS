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