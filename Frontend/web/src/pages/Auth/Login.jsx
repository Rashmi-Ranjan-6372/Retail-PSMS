import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import { Box, Button, FormControl, Input, Text } from "@chakra-ui/react";
import { loginUser } from "../../api/authAPI";
import useAuth from "../../hooks/useAuth";
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
} from "../../styles/common/forms";
import { primaryButton } from "../../styles/common/buttons";
import { heading2, subtitle } from "../../styles/common/typography";

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const [focusedField, setFocusedField] = useState("");

  const [showPassword, setShowPassword] = useState(false);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");

    if (!formData.username || !formData.password) {
      setError("Please enter username and password");
      return;
    }

    try {
      setLoading(true);

      const res = await loginUser(formData);

      if (res.data.otp_required) {
        navigate("/verify-otp", {
          state: {
            user_id: res.data.user_id,
            username: formData.username,
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
    <Box sx={pageContainer}>
      <Background />

      <Box sx={glassCard}>
        <Text sx={heading2} textAlign="center" mb="5px">
          🔐 Welcome Back
        </Text>

        <Text sx={subtitle} textAlign="center" mb="28px">
          Login to continue
        </Text>

        {error && <Box sx={errorAlert}>{error}</Box>}

        <Box as="form" sx={form} onSubmit={handleSubmit}>
          <FormControl sx={formGroup}>
            <Input
              sx={textInput}
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              onFocus={() => setFocusedField("username")}
              onBlur={() => setFocusedField("")}
            />

            <Text
              as="label"
              sx={{
                ...floatingLabel,
                ...(focusedField === "username" || formData.username
                  ? floatingLabelActive
                  : {}),
              }}
            >
              Username
            </Text>
          </FormControl>
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
              Password
            </Text>

            <Box
              sx={inputAction}
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </Box>
          </FormControl>

          <Button type="submit" sx={primaryButton} disabled={loading}>
            {loading ? (
              <Box
                display="flex"
                alignItems="center"
                justifyContent="center"
                gap="10px"
              >
                <Loader size="18px" />
                <Text color="white" fontSize="15px" fontWeight="600">
                  Logging in...
                </Text>
              </Box>
            ) : (
              "Login"
            )}
          </Button>
        </Box>
      </Box>
    </Box>
  );
};

export default Login;
