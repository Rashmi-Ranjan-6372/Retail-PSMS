import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Link, Text } from "@chakra-ui/react";
import { loginUser } from "../../api/authAPI";
import useAuth from "../../hooks/useAuth";
import Background from "../../components/common/Background";
import { PrimaryButton } from "../../components/common/buttons";
import { TextInput, PasswordInput } from "../../components/common/inputs";
import { pageContainer, linkContainer } from "../../styles/common/layout";
import { glassCard } from "../../styles/components/cards";
import { form } from "../../styles/components/forms";
import { errorAlert } from "../../styles/components/alerts";
import { link, pageSubtitle, pageTitle } from "../../styles/common/typography";

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

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

    if (!formData.username.trim() || !formData.password.trim()) {
      setError("Please enter username and password.");
      return;
    }

    try {
      setLoading(true);

      const { data } = await loginUser(formData);

      if (data.otp_required) {
        navigate("/verify-otp", {
          state: {
            user_id: data.user_id,
            username: formData.username,
          },
        });
        return;
      }

      if (data.success) {
        login(data);
        navigate("/dashboard");
        return;
      }

      setError(data.message || "Invalid username or password.");
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
        <Text sx={pageTitle}>🔐 Welcome Back</Text>

        <Text sx={pageSubtitle}>
          Login to continue
        </Text>

        {error && <Box sx={errorAlert}>{error}</Box>}

        <Box as="form" sx={form} onSubmit={handleSubmit} mt={6}>
          <TextInput
            label="Username"
            name="username"
            value={formData.username}
            onChange={handleChange}
          />

          <PasswordInput
            label="Password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />

          <Box display="flex" justifyContent="flex-end" mt={1} mb={4}>
            <Link sx={link} onClick={() => navigate("/forgot-password")}>
              Forgot Password?
            </Link>
          </Box>

          <PrimaryButton
            type="submit"
            isLoading={loading}
            loadingText="Logging in..."
          >
            Login
          </PrimaryButton>
        </Box>
      </Box>
    </Box>
  );
};

export default Login;
