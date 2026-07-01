import { useEffect, useRef, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { verifyOTP, resendOTP } from "../../api/authAPI";
import useAuth from "../../hooks/useAuth";

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
    if (
      e.key === "Backspace" &&
      otp[index] === "" &&
      index > 0
    ) {
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

    const next = Math.min(values.length, 5);
    inputRefs.current[next]?.focus();
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
      setError(
        err.response?.data?.message ||
          "OTP verification failed."
      );
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
        setMessage(
          "A new OTP has been sent to your registered email."
        );

        setOtp(["", "", "", "", "", ""]);
        inputRefs.current[0]?.focus();
      } else {
        setError(res.data.message);
      }
    } catch (err) {
      setError(
        err.response?.data?.message ||
          "Unable to resend OTP."
      );
    } finally {
      setResending(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>Email Verification</h2>

        <p style={styles.subtitle}>
          Enter the 6-digit OTP sent to your registered email.
        </p>

        {error && <div style={styles.error}>{error}</div>}
        {message && <div style={styles.success}>{message}</div>}

        <form onSubmit={handleVerify}>
          <div style={styles.otpContainer}>
            {otp.map((digit, index) => (
              <input
                key={index}
                ref={(el) => (inputRefs.current[index] = el)}
                value={digit}
                maxLength={1}
                type="text"
                inputMode="numeric"
                onChange={(e) =>
                  handleChange(e.target.value, index)
                }
                onKeyDown={(e) =>
                  handleKeyDown(e, index)
                }
                onPaste={handlePaste}
                style={styles.otpInput}
              />
            ))}
          </div>

          <button
            type="submit"
            style={styles.button}
            disabled={loading}
          >
            {loading ? "Verifying..." : "Verify OTP"}
          </button>
        </form>

        <button
          type="button"
          style={styles.resendButton}
          disabled={resending}
          onClick={handleResend}
        >
          {resending ? "Sending..." : "Resend OTP"}
        </button>

        <button
          type="button"
          style={styles.backButton}
          onClick={() => navigate("/login")}
        >
          Back to Login
        </button>
      </div>
    </div>
  );
};

export default VerifyOTP;

const styles = {
  container: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg,#F8FAFC,#EEF6FF)",
    padding: "20px",
    fontFamily: "Inter, Arial",
  },

  card: {
    width: "100%",
    maxWidth: "430px",
    background: "#fff",
    padding: "35px",
    borderRadius: "16px",
    boxShadow: "0 10px 30px rgba(0,0,0,.08)",
  },

  title: {
    textAlign: "center",
    marginBottom: "10px",
    color: "#1E293B",
  },

  subtitle: {
    textAlign: "center",
    color: "#64748B",
    marginBottom: "20px",
  },

  user: {
    textAlign: "center",
    marginBottom: "20px",
    color: "#334155",
  },

  otpContainer: {
    display: "flex",
    justifyContent: "space-between",
    gap: "10px",
    marginBottom: "25px",
  },

  otpInput: {
    width: "52px",
    height: "58px",
    border: "1px solid #CBD5E1",
    borderRadius: "10px",
    textAlign: "center",
    fontSize: "24px",
    fontWeight: "600",
    outline: "none",
  },

  button: {
    width: "100%",
    padding: "13px",
    border: "none",
    borderRadius: "10px",
    background: "#2563EB",
    color: "#fff",
    fontWeight: "600",
    cursor: "pointer",
    marginBottom: "15px",
    fontSize: "15px",
  },

  resendButton: {
    width: "100%",
    padding: "13px",
    border: "1px solid #2563EB",
    background: "#fff",
    color: "#2563EB",
    borderRadius: "10px",
    cursor: "pointer",
    marginBottom: "12px",
    fontWeight: "600",
  },

  backButton: {
    width: "100%",
    padding: "13px",
    border: "none",
    background: "#E2E8F0",
    borderRadius: "10px",
    cursor: "pointer",
    fontWeight: "600",
  },

  error: {
    background: "#FEE2E2",
    color: "#DC2626",
    padding: "10px",
    borderRadius: "8px",
    marginBottom: "15px",
    textAlign: "center",
  },

  success: {
    background: "#DCFCE7",
    color: "#15803D",
    padding: "10px",
    borderRadius: "8px",
    marginBottom: "15px",
    textAlign: "center",
  },
};