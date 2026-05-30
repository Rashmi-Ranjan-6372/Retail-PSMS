import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../../API/authAPI";
import useAuth from "../../hooks/useAuth";

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
          <div style={styles.inputGroup}>
            <label style={styles.label}>Username</label>
            <input
              type="text"
              name="username"
              placeholder="Enter username"
              value={form.username}
              onChange={handleChange}
              style={styles.input}
            />
          </div>

          {/* Password */}
          <div style={styles.inputGroup}>
            <label style={styles.label}>Password</label>
            <div style={{ position: "relative" }}>
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Enter password"
                value={form.password}
                onChange={handleChange}
                style={styles.input}
              />
              <span
                onClick={() => setShowPassword(!showPassword)}
                style={styles.toggle}
              >
                {showPassword ? "🙈" : "👁"}
              </span>
            </div>
          </div>

          {/* Button */}
          <button type="submit" style={styles.button} disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
};                                                                                                                                                                                               

export default Login;





// ================= STYLES ================= //

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#CBD0DD",
    fontFamily: "Inter, Arial, sans-serif",
  },

  card: {
    width: "420px",
    padding: "40px",
    borderRadius: "20px",
    background: "#FFFFFF",
    border: "1px solid #B8C0D0",
    boxShadow: "0 10px 25px rgba(0, 0, 0, 0.08)",
  },

  logo: {
    textAlign: "center",
    fontSize: "52px",
    marginBottom: "12px",
  },

  title: {
    color: "#1E293B",
    marginBottom: "6px",
    textAlign: "center",
    fontSize: "30px",
    fontWeight: "700",
  },

  subtitle: {
    color: "#64748B",
    marginBottom: "28px",
    textAlign: "center",
    fontSize: "14px",
  },

  inputGroup: {
    marginBottom: "18px",
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
    padding: "14px",
    borderRadius: "10px",
    border: "1px solid #CBD0DD",
    background: "#F8FAFC",
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
    padding: "14px",
    marginTop: "14px",
    borderRadius: "10px",
    border: "none",
    background: "#3B82F6",
    color: "#FFFFFF",
    fontWeight: "700",
    fontSize: "15px",
    cursor: "pointer",
    boxShadow: "0 4px 12px rgba(59,130,246,0.25)",
    transition: "all 0.2s ease",
  },

  error: {
    background: "#FEF2F2",
    color: "#DC2626",
    padding: "12px",
    borderRadius: "8px",
    marginBottom: "15px",
    border: "1px solid #FECACA",
    fontSize: "14px",
  },

  footer: {
    textAlign: "center",
    marginTop: "20px",
    color: "#64748B",
    fontSize: "12px",
  },

  version: {
    textAlign: "center",
    color: "#94A3B8",
    fontSize: "11px",
    marginTop: "5px",
  },
};