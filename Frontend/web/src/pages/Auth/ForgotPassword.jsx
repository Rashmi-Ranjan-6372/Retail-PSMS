import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Button, FormControl, Input, Text } from "@chakra-ui/react";
import { forgotPassword } from "../../api/authAPI";
import Loader from "../../components/common/Loader";
import Background from "../../components/common/Background";
import { pageContainer } from "../../styles/common/layout";
import { glassCard } from "../../styles/common/cards";

import {
  form,
  formGroup,
  textInput,
  floatingLabel,
  floatingLabelActive,
  errorAlert,
  successAlert,
} from "../../styles/common/forms";

import { primaryButton, ghostFullButton } from "../../styles/common/buttons";
import { heading2, subtitle } from "../../styles/common/typography";

const ForgotPassword = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [focused, setFocused] = useState(false);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setMessage("");

    if (!email.trim()) {
      setError("Please enter your registered email.");
      return;
    }

    try {
      setLoading(true);

      const res = await forgotPassword({
        email,
      });

      if (res.data.success) {
        setMessage(
          "Password reset link has been sent to your registered email.",
        );
      } else {
        setError(res.data.message);
      }
    } catch (err) {
      setError(
        err.response?.data?.message || "Unable to send password reset email.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={pageContainer}>
      <Background />

      <Box sx={glassCard}>
        <Text sx={heading2} textAlign="center" mb="6px">
          Forgot Password
        </Text>

        <Text sx={subtitle} textAlign="center" mb="28px">
          Enter your registered email address to receive a password reset link.
        </Text>

        {error && <Box sx={errorAlert}>{error}</Box>}

        {message && <Box sx={successAlert}>{message}</Box>}

        <Box as="form" sx={form} onSubmit={handleSubmit}>
          <FormControl sx={formGroup}>
            <Input
              sx={textInput}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
            />

            <Text
              as="label"
              sx={{
                ...floatingLabel,
                ...(focused || email ? floatingLabelActive : {}),
              }}
            >
              Registered Email
            </Text>
          </FormControl>

          <Button type="submit" sx={primaryButton} isDisabled={loading}>
            {loading ? (
              <Box
                display="flex"
                alignItems="center"
                justifyContent="center"
                gap="10px"
              >
                <Loader size="18px" />

                <Text color="white" fontSize="15px" fontWeight="600">
                  Sending...
                </Text>
              </Box>
            ) : (
              "Send Reset Link"
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
    </Box>
  );
};

export default ForgotPassword;
