import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Box, Text } from "@chakra-ui/react";

import { resetPassword } from "../../api/authAPI";

import Background from "../../components/common/Background";
import { PasswordInput } from "../../components/common/inputs";
import {
  PrimaryButton,
  SecondaryButton,
} from "../../components/common/buttons";

import { pageContainer } from "../../styles/common/layout";
import { glassCard } from "../../styles/components/cards";
import { form } from "../../styles/components/forms";
import { errorAlert, successAlert } from "../../styles/components/alerts";
import { pageTitle, pageSubtitle } from "../../styles/common/typography";

const ResetPassword = () => {
  const navigate = useNavigate();
  const { uid, token } = useParams();

  const [formData, setFormData] = useState({
    password: "",
    confirm_password: "",
  });

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    if (!formData.password.trim() || !formData.confirm_password.trim()) {
      setError("Please fill all fields.");
      return;
    }

    if (formData.password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    if (formData.password !== formData.confirm_password) {
      setError("Passwords do not match.");
      return;
    }

    try {
      setLoading(true);

      const { data } = await resetPassword({
        uid,
        token,
        password: formData.password,
      });

      if (data.success) {
        setSuccess("Password reset successfully. Redirecting to Login...");

        setTimeout(() => {
          navigate("/login");
        }, 2000);

        return;
      }

      setError(data.message || "Unable to reset password.");
    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.detail ||
          "Password reset failed.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={pageContainer}>
      <Background />

      <Box sx={glassCard}>
        <Text sx={pageTitle}>🔒 Reset Password</Text>

        <Text sx={pageSubtitle}>Enter your new password to continue.</Text>

        {error && <Box sx={errorAlert}>{error}</Box>}

        {success && <Box sx={successAlert}>{success}</Box>}

        <Box as="form" sx={form} onSubmit={handleSubmit}>
          <PasswordInput
            label="New Password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />

          <PasswordInput
            label="Confirm Password"
            name="confirm_password"
            value={formData.confirm_password}
            onChange={handleChange}
          />

          <PrimaryButton
            type="submit"
            isLoading={loading}
            loadingText="Resetting Password..."
          >
            Reset Password
          </PrimaryButton>

          <SecondaryButton type="button" onClick={() => navigate("/login")}>
            Back to Login
          </SecondaryButton>
        </Box>
      </Box>
    </Box>
  );
};

export default ResetPassword;
