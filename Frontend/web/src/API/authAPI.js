import api from "./api";
import { ENDPOINTS } from "./endpoints";

export const loginUser = (data) => {
  return api.post(ENDPOINTS.LOGIN, data);
};