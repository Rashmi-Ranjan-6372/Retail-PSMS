import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import { Box, Button, FormControl, Input, Text } from "@chakra-ui/react";
import { resetPassword } from "../../api/authAPI";
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
  inputAction,
  errorAlert,
  successAlert,
} from "../../styles/common/forms";

import { primaryButton, ghostFullButton } from "../../styles/common/buttons";

import { heading2, subtitle } from "../../styles/common/typography";

const ResetPassword = () => {
  const navigate = useNavigate();
  const { uid, token } = useParams();

  const [formData, setFormData] = useState({
    password: "",
    confirm_password: "",
  });

  const [focusedField, setFocusedField] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

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

    if (!formData.password || !formData.confirm_password) {
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

      const res = await resetPassword({
        uid,
        token,
        password: formData.password,
      });

      if (res.data.success) {
        setSuccess("Password reset successfully. Redirecting to Login...");

        setTimeout(() => {
          navigate("/login");
        }, 2000);

        return;
      }

      setError(res.data.message || "Unable to reset password.");
    } catch (err) {
      setError(err.response?.data?.message || "Password reset failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={pageContainer}>
      <Background />

      <Box sx={glassCard}>
        <Text sx={heading2} textAlign="center" mb="6px">
          🔒 Reset Password
        </Text>

        <Text sx={subtitle} textAlign="center" mb="28px">
          Enter your new password.
        </Text>

        {error && <Box sx={errorAlert}>{error}</Box>}

        {success && <Box sx={successAlert}>{success}</Box>}

        <Box as="form" sx={form} onSubmit={handleSubmit}>
          <FormControl sx={formGroup}>
            <Input
              sx={textInput}
              type={showPassword ? "text" : "password"}
              name="password"
              value={formData.password}
              onChange={handleChange}
              onFocus={() => setFocusedField("password")}
              onBlur={() => setFocusedField("")}
            />

            <Text
              as="label"
              sx={{
                ...floatingLabel,
                ...(focusedField === "password" || formData.password
                  ? floatingLabelActive
                  : {}),
              }}
            >
              New Password
            </Text>

            <Box
              sx={inputAction}
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </Box>
          </FormControl>

          <FormControl sx={formGroup}>
            <Input
              sx={textInput}
              type={showConfirmPassword ? "text" : "password"}
              name="confirm_password"
              value={formData.confirm_password}
              onChange={handleChange}
              onFocus={() => setFocusedField("confirm_password")}
              onBlur={() => setFocusedField("")}
            />

            <Text
              as="label"
              sx={{
                ...floatingLabel,
                ...(focusedField === "confirm_password" ||
                formData.confirm_password
                  ? floatingLabelActive
                  : {}),
              }}
            >
              Confirm Password
            </Text>

            <Box
              sx={inputAction}
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            >
              {showConfirmPassword ? <FaEyeSlash /> : <FaEye />}
            </Box>
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
                  Resetting Password...
                </Text>
              </Box>
            ) : (
              "Reset Password"
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

export default ResetPassword;
