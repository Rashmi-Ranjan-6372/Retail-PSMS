import { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  FormControl,
  HStack,
  Input,
  Text,
} from "@chakra-ui/react";
import { verifyOTP, resendOTP } from "../../api/authAPI";
import useAuth from "../../hooks/useAuth";
import Loader from "../../components/common/Loader";
import Background from "../../components/common/Background";
import { pageContainer } from "../../styles/common/layout";
import { glassCard } from "../../styles/common/cards";
import { form, pinContainer, pinInput } from "../../styles/common/forms";
import { errorAlert, successAlert } from "../../styles/common/alerts";
import {
  primaryButton,
  secondaryButton,
  ghostFullButton,
} from "../../styles/common/buttons";
import { buttonLoader } from "../../styles/common/loader";
import {
  pageTitle,
  pageSubtitle,
  whiteButtonText,
  body,
} from "../../styles/common/typography";

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
      return;
    }

    inputRefs.current[0]?.focus();
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
    <Box sx={pageContainer}>
      <Background />

      <Box sx={glassCard}>
        <Text sx={pageTitle}>Email Verification</Text>

        <Text sx={pageSubtitle}>
          Enter the 6-digit OTP sent to your registered email.
        </Text>

        {username && (
          <Text sx={body} textAlign="center" mb={6}>
            User: <strong>{username}</strong>
          </Text>
        )}

        {error && <Box sx={errorAlert}>{error}</Box>}

        {message && <Box sx={successAlert}>{message}</Box>}

        <Box as="form" sx={form} onSubmit={handleVerify}>
          <HStack sx={pinContainer}>
            {otp.map((digit, index) => (
              <FormControl key={index}>
                <Input
                  ref={(el) => (inputRefs.current[index] = el)}
                  value={digit}
                  maxLength={1}
                  type="text"
                  inputMode="numeric"
                  sx={pinInput}
                  onChange={(e) => handleChange(e.target.value, index)}
                  onKeyDown={(e) => handleKeyDown(e, index)}
                  onPaste={handlePaste}
                />
              </FormControl>
            ))}
          </HStack>

          <Button type="submit" sx={primaryButton} isDisabled={loading} mt={2}>
            {loading ? (
              <Box sx={buttonLoader}>
                <Loader size="18px" />
                <Text sx={whiteButtonText}>Verifying...</Text>
              </Box>
            ) : (
              "Verify OTP"
            )}
          </Button>
        </Box>

        <Button
          sx={secondaryButton}
          mt={4}
          onClick={handleResend}
          isDisabled={resending}
        >
          {resending ? (
            <Box sx={buttonLoader}>
              <Loader size="18px" />
              <Text>Sending...</Text>
            </Box>
          ) : (
            "Resend OTP"
          )}
        </Button>

        <Button
          type="button"
          sx={ghostFullButton}
          onClick={() => navigate("/login")}
        >
          Back to Login
        </Button>
      </Box>
    </Box>
  );
};

export default VerifyOTP;
