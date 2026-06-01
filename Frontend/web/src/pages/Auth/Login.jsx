import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../../API/authAPI";
import useAuth from "../../hooks/useAuth";
import { FaEye, FaEyeSlash } from "react-icons/fa";
const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [focusedField, setFocusedField] = useState("");
  // Handle input change
  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  // Handle login
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Validation
    if (!form.username || !form.password) {
      setError("Please enter username and password");
      return;
    }

    try {
      setLoading(true);

      const res = await loginUser(form);

      if (res?.data?.success) {
        login(res.data); // store token/user
        navigate("/dashboard");
      } else {
        setError(res?.data?.message || "Invalid credentials");
      }
    } catch (err) {
      setError("Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>🔐 Welcome Back</h2>
        <p style={styles.subtitle}>Login to continue</p>

        {error && <div style={styles.error}>{error}</div>}

        <form onSubmit={handleSubmit}>
          {/* Username */}
          <div style={styles.field}>
            <input
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              onFocus={() => setFocusedField("username")}
              onBlur={() => setFocusedField("")}
              style={styles.input}
            />

            <label
              style={{
                ...styles.floatingLabel,
                ...(focusedField === "username" || form.username
                  ? styles.floatingLabelActive
                  : {}),
              }}
            >
              Username
            </label>
          </div>

          {/* Password */}
          <div style={styles.field}>
            <input
              type={showPassword ? "text" : "password"}
              name="password"
              value={form.password}
              onChange={handleChange}
              onFocus={() => setFocusedField("password")}
              onBlur={() => setFocusedField("")}
              style={styles.input}
            />

            <label
              style={{
                ...styles.floatingLabel,
                ...(focusedField === "password" || form.password
                  ? styles.floatingLabelActive
                  : {}),
              }}
            >
              Password
            </label>

            <span
              onClick={() => setShowPassword(!showPassword)}
              style={styles.toggle}
            >
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </span>
          </div>

          {/* Login Button */}
          <button
            type="submit"
            style={styles.button}
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form >
      </div >
    </div >
  );
};

export default Login;





// ================= STYLES ================= //

const styles = {
  container: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #F8FAFC 0%, #EEF6FF 100%)",
    padding: "20px",
    fontFamily: "Inter, Arial, sans-serif",
  },

  card: {
    width: "100%",
    maxWidth: "450px",
    padding: "30px",
    borderRadius: "16px",
    background: "#FFFFFF",
    border: "1px solid #E2E8F0",
    boxShadow: "0 10px 25px rgba(0,0,0,0.08)",
    boxSizing: "border-box",
  },
  field: {
    position: "relative",
    marginBottom: "24px",
  },

  floatingLabel: {
    position: "absolute",
    left: "14px",
    top: "16px",
    color: "#94A3B8",
    fontSize: "14px",
    transition: "all 0.2s ease",
    pointerEvents: "none",
    background: "#FFFFFF",
  },

  floatingLabelActive: {
    top: "-10px",
    left: "12px",
    padding: "0 6px",
    fontSize: "12px",
    color: "#2563EB",
    fontWeight: "600",
  },
  logo: {
    textAlign: "center",
    fontSize: "48px",
    marginBottom: "10px",
  },

  title: {
    color: "#1E293B",
    marginBottom: "4px",
    textAlign: "center",
    fontSize: "24px",
    fontWeight: "700",
  },

  subtitle: {
    color: "#64748B",
    marginBottom: "24px",
    textAlign: "center",
    fontSize: "14px",
  },

  inputGroup: {
    marginBottom: "16px",
    textAlign: "left",
  },

  label: {
    display: "block",
    color: "#334155",
    marginBottom: "6px",
    fontSize: "14px",
    fontWeight: "600",
  },

  input: {
    width: "100%",
    height: "52px",
    padding: "18px 14px 0px 14px",
    borderRadius: "8px",
    border: "1.5px solid #94A3B8",
    background: "#FFFFFF",
    color: "#1E293B",
    outline: "none",
    boxSizing: "border-box",
    fontSize: "14px",
    transition: "all 0.2s ease",
  },

  toggle: {
    position: "absolute",
    right: "12px",
    top: "50%",
    transform: "translateY(-50%)",
    cursor: "pointer",
    color: "#64748B",
  },

  button: {
    width: "100%",
    padding: "12px",
    marginTop: "12px",
    borderRadius: "8px",
    border: "none",
    background: "#2563EB",
    color: "#FFFFFF",
    fontWeight: "700",
    fontSize: "15px",
    cursor: "pointer",
    boxShadow: "0 4px 12px rgba(37,99,235,0.25)",
  },

  error: {
    background: "#FEF2F2",
    color: "#DC2626",
    padding: "12px",
    borderRadius: "8px",
    marginBottom: "16px",
    border: "1px solid #FECACA",
    fontSize: "14px",
  },
};