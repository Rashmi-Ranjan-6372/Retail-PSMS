import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Button, FormControl, Text } from "@chakra-ui/react";

import { forgotPassword } from "../../api/authAPI";

import Background from "../../components/common/Background";
import Spinner from "../../components/common/loaders/Spinner";
import { TextInput } from "../../components/common/inputs";

import { pageContainer } from "../../styles/common/layout";
import { glassCard } from "../../styles/components/cards";
import { form, formGroup } from "../../styles/components/forms";
import { errorAlert, successAlert } from "../../styles/components/alerts";
import { primaryButton, ghostButton } from "../../styles/components/buttons";
import { buttonLoader } from "../../styles/components/loaders";
import {
  pageTitle,
  pageSubtitle,
  whiteButtonText,
} from "../../styles/common/typography";

const ForgotPassword = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
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

      const { data } = await forgotPassword({ email });

      if (data.success) {
        setMessage(
          "Password reset link has been sent to your registered email.",
        );
      } else {
        setError(data.message || "Something went wrong.");
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
        <Text sx={pageTitle}>Forgot Password</Text>

        <Text sx={pageSubtitle}>
          Enter your registered email address to receive a password reset link.
        </Text>

        {error && <Box sx={errorAlert}>{error}</Box>}

        {message && <Box sx={successAlert}>{message}</Box>}

        <Box as="form" sx={form} onSubmit={handleSubmit}>
          <FormControl sx={formGroup}>
            <TextInput
              label="Registered Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </FormControl>

          <Button
            type="submit"
            sx={primaryButton}
            isLoading={loading}
            loadingText="Sending..."
          >
            {!loading && "Send Reset Link"}
          </Button>

          <Button
            type="button"
            sx={ghostButton}
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
