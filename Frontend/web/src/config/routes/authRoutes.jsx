import Login from "../../pages/Auth/Login";
import VerifyOTP from "../../pages/Auth/VerifyOTP";

export const authRoutes = [
  {
    path: "/login",
    component: Login,
    public: true,
  },
  {
    path: "/verify-otp",
    component: VerifyOTP,
    public: true,
  },
];