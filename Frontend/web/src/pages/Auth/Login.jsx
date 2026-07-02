import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaEye, FaEyeSlash } from "react-icons/fa";

import { loginUser } from "../../api/authAPI";
import useAuth from "../../hooks/useAuth";

import Capsule from "../../assets/pharmacy-icons/capsule-medicine.svg";
import MedicineCross from "../../assets/pharmacy-icons/medical-cross.svg";
import Hospital from "../../assets/pharmacy-icons/hospital.svg";
import Pill from "../../assets/pharmacy-icons/pill.svg";
import Prescription from "../../assets/pharmacy-icons/prescription.svg";
import Stethoscope from "../../assets/pharmacy-icons/stethoscope.svg";
import Syringe from "../../assets/pharmacy-icons/syringe-medical.svg";
import Doctor from "../../assets/pharmacy-icons/doctor-man.svg";
import Monitor from "../../assets/pharmacy-icons/health-monitor.svg";
import HospitalLocation from "../../assets/pharmacy-icons/hospital-location.svg";
import PatientBed from "../../assets/pharmacy-icons/patient-bed.svg";
import Temperature from "../../assets/pharmacy-icons/temperature.svg";

import "../../styles/auth/Login.css";

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [focusedField, setFocusedField] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");

    if (!form.username || !form.password) {
      setError("Please enter username and password");
      return;
    }

    try {
      setLoading(true);

      const res = await loginUser(form);

      if (res.data.otp_required) {
        navigate("/verify-otp", {
          state: {
            user_id: res.data.user_id,
            username: form.username,
          },
        });
        return;
      }

      if (res.data.success) {
        login(res.data);
        navigate("/dashboard");
        return;
      }

      setError(res.data.message || "Invalid username or password");
    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.detail ||
          "Login failed. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
        <div className="pharmacy-bg">
            <img src={Capsule} className="bg-icon icon1" alt="" />
            <img src={MedicineCross} className="bg-icon icon2" alt="" />
            <img src={Hospital} className="bg-icon icon3" alt="" />
            <img src={Pill} className="bg-icon icon4" alt="" />
            <img src={Prescription} className="bg-icon icon5" alt="" />
            <img src={Stethoscope} className="bg-icon icon6" alt="" />
            <img src={Syringe} className="bg-icon icon7" alt="" />
            <img src={Doctor} className="bg-icon icon8" alt="" />
            <img src={Monitor} className="bg-icon icon9" alt="" />
            <img src={HospitalLocation} className="bg-icon icon10" alt="" />
            <img src={PatientBed} className="bg-icon icon11" alt="" />
            <img src={Temperature} className="bg-icon icon12" alt="" />
        </div>
      <div className="login-card">
        <h2 className="login-title">🔐 Welcome Back</h2>

        <p className="login-subtitle">Login to continue</p>

        {error && <div className="login-error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="login-field">
            <input
              className="login-input"
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              onFocus={() => setFocusedField("username")}
              onBlur={() => setFocusedField("")}
            />

            <label
              className={`login-label ${
                focusedField === "username" || form.username ? "active" : ""
              }`}
            >
              Username
            </label>
          </div>

          <div className="login-field">
            <input
              className="login-input"
              type={showPassword ? "text" : "password"}
              name="password"
              value={form.password}
              onChange={handleChange}
              onFocus={() => setFocusedField("password")}
              onBlur={() => setFocusedField("")}
            />

            <label
              className={`login-label ${
                focusedField === "password" || form.password ? "active" : ""
              }`}
            >
              Password
            </label>

            <span
              className="password-toggle"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </span>
          </div>

          <button className="login-button" type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
