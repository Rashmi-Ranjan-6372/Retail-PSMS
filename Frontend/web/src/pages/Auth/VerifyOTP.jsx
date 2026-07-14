import { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Box, HStack, Input, Text } from "@chakra-ui/react";
import { verifyOTP, resendOTP } from "../../api/authAPI";
import useAuth from "../../hooks/useAuth";
import Background from "../../components/common/Background";
import {
  PrimaryButton,
  SecondaryButton,
} from "../../components/common/buttons";
import { pageContainer } from "../../styles/common/layout";
import { glassCard } from "../../styles/components/cards";
import { form } from "../../styles/components/forms";
import { pinContainer, pinInput } from "../../styles/components/inputs";
import { errorAlert, successAlert } from "../../styles/components/alerts";
import { pageTitle, pageSubtitle, body } from "../../styles/common/typography";

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
      navigate("/login", { replace: true });
      return;
    }

    inputRefs.current[0]?.focus();
  }, [user_id, navigate]);

  const handleChange = (value, index) => {
    if (!/^\d?$/.test(value)) return;

    const updated = [...otp];
    updated[index] = value;

    setOtp(updated);

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
    const updated = [...otp];

    values.forEach((digit, i) => {
      updated[i] = digit;
    });

    setOtp(updated);

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

      const { data } = await verifyOTP({
        user_id,
        otp: otpValue,
      });

      if (data.success) {
        login({
          user: data.user,
          tokens: {
            access: data.access,
            refresh: data.refresh,
          },
        });

        navigate("/dashboard", {
          replace: true,
        });

        return;
      }

      setError(data.message || "Invalid OTP.");
    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.detail ||
          "OTP verification failed.",
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

      const { data } = await resendOTP({
        user_id,
      });

      if (data.success) {
        setMessage("A new OTP has been sent to your registered email.");

        setOtp(["", "", "", "", "", ""]);

        inputRefs.current[0]?.focus();
      } else {
        setError(data.message || "Unable to resend OTP.");
      }
    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.detail ||
          "Unable to resend OTP.",
      );
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
              <Input
                key={index}
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
            ))}
          </HStack>

          <PrimaryButton
            mt={6}
            type="submit"
            isLoading={loading}
            loadingText="Verifying..."
          >
            Verify OTP
          </PrimaryButton>
        </Box>

        <SecondaryButton
          mt={4}
          isLoading={resending}
          loadingText="Sending..."
          onClick={handleResend}
        >
          Resend OTP
        </SecondaryButton>

        <SecondaryButton
          mt={3}
          variant="ghost"
          onClick={() => navigate("/login")}
        >
          Back to Login
        </SecondaryButton>
      </Box>
    </Box>
  );
};

export default VerifyOTP;
