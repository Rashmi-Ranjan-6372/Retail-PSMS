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
    background: "linear-gradient(135deg, #0f172a, #1e293b)",
    fontFamily: "Arial, sans-serif",
  },

  card: {
    width: "360px",
    padding: "30px",
    borderRadius: "12px",
    background: "#1e293b",
    boxShadow: "0 10px 30px rgba(0,0,0,0.6)",
    textAlign: "center",
  },

  title: {
    color: "#e2e8f0",
    marginBottom: "5px",
  },

  subtitle: {
    color: "#94a3b8",
    marginBottom: "20px",
    fontSize: "14px",
  },

  inputGroup: {
    marginBottom: "15px",
    textAlign: "left",
  },

  label: {
    display: "block",
    color: "#cbd5f5",
    marginBottom: "5px",
    fontSize: "14px",
  },

  input: {
    width: "100%",
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #334155",
    background: "#0f172a",
    color: "#fff",
    outline: "none",
  },

  toggle: {
    position: "absolute",
    right: "10px",
    top: "50%",
    transform: "translateY(-50%)",
    cursor: "pointer",
  },

  button: {
    width: "100%",
    padding: "12px",
    marginTop: "10px",
    borderRadius: "8px",
    border: "none",
    background: "linear-gradient(90deg, #06b6d4, #3b82f6)",
    color: "#fff",
    fontWeight: "bold",
    cursor: "pointer",
  },

  error: {
    background: "#ef4444",
    color: "#fff",
    padding: "10px",
    borderRadius: "6px",
    marginBottom: "15px",
    fontSize: "14px",
  },
};