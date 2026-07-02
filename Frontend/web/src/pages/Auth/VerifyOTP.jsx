import { useEffect, useRef, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { verifyOTP, resendOTP } from "../../api/authAPI";
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

import "../../styles/auth/VerifyOTP.css";

const VerifyOTP = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const user_id = location.state?.user_id;
  const username = location.state?.username;

  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const inputRefs = useRef([]);

  useEffect(() => {
    if (!user_id) {
      navigate("/login");
    } else {
      inputRefs.current[0]?.focus();
    }
  }, [user_id, navigate]);

  const handleChange = (value, index) => {
    if (!/^\d?$/.test(value)) return;

    const updatedOTP = [...otp];
    updatedOTP[index] = value;
    setOtp(updatedOTP);

    if (value && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (e, index) => {
    if (e.key === "Backspace" && otp[index] === "" && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handlePaste = (e) => {
    e.preventDefault();

    const pasted = e.clipboardData
      .getData("text")
      .replace(/\D/g, "")
      .slice(0, 6);

    if (!pasted) return;

    const values = pasted.split("");
    const updatedOTP = [...otp];

    values.forEach((digit, i) => {
      updatedOTP[i] = digit;
    });

    setOtp(updatedOTP);

    inputRefs.current[Math.min(values.length, 5)]?.focus();
  };

  const handleVerify = async (e) => {
    e.preventDefault();

    setError("");
    setMessage("");

    const otpValue = otp.join("");

    if (otpValue.length !== 6) {
      setError("Please enter the complete 6-digit OTP.");
      return;
    }

    try {
      setLoading(true);

      const res = await verifyOTP({
        user_id,
        otp: otpValue,
      });

      if (res.data.success) {
        login({
          user: res.data.user,
          tokens: {
            access: res.data.access,
            refresh: res.data.refresh,
          },
        });

        navigate("/dashboard", {
          replace: true,
        });

        return;
      }

      setError(res.data.message || "Invalid OTP.");
    } catch (err) {
      setError(err.response?.data?.message || "OTP verification failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    try {
      setResending(true);
      setError("");
      setMessage("");

      const res = await resendOTP({
        user_id,
      });

      if (res.data.success) {
        setMessage("A new OTP has been sent to your registered email.");
        setOtp(["", "", "", "", "", ""]);
        inputRefs.current[0]?.focus();
      } else {
        setError(res.data.message);
      }
    } catch (err) {
      setError(err.response?.data?.message || "Unable to resend OTP.");
    } finally {
      setResending(false);
    }
  };

  return (
    <div className="otp-container">
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
      <div className="otp-card">
        <h2 className="otp-title">Email Verification</h2>

        <p className="otp-subtitle">
          Enter the 6-digit OTP sent to your registered email.
        </p>

        {error && <div className="otp-error">{error}</div>}
        {message && <div className="otp-success">{message}</div>}

        <form onSubmit={handleVerify}>
          <div className="otp-input-container">
            {otp.map((digit, index) => (
              <input
                key={index}
                ref={(el) => (inputRefs.current[index] = el)}
                value={digit}
                maxLength={1}
                type="text"
                inputMode="numeric"
                className="otp-input"
                onChange={(e) => handleChange(e.target.value, index)}
                onKeyDown={(e) => handleKeyDown(e, index)}
                onPaste={handlePaste}
              />
            ))}
          </div>

          <button type="submit" className="otp-button" disabled={loading}>
            {loading ? "Verifying..." : "Verify OTP"}
          </button>
        </form>

        <button
          type="button"
          className="otp-resend"
          disabled={resending}
          onClick={handleResend}
        >
          {resending ? "Sending..." : "Resend OTP"}
        </button>

        <button
          type="button"
          className="otp-back"
          onClick={() => navigate("/login")}
        >
          Back to Login
        </button>
      </div>
    </div>
  );
};

export default VerifyOTP;
