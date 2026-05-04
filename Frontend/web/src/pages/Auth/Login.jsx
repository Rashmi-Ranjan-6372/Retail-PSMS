import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../../API/authAPI";
import useAuth from "../../hooks/useAuth";

const Login = () => {
  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const navigate = useNavigate();
  const { login } = useAuth();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      const res = await loginUser(form);

      if (res.data.success) {
        login(res.data);   

        navigate("/dashboard");
      }
    } catch (err) {
      alert("Invalid credentials");
    }
  };

  return (
    <div>
      <h2>Login</h2>

      <input name="username" onChange={handleChange} />
      <input name="password" type="password" onChange={handleChange} />

      <button onClick={handleSubmit}>Login</button>
    </div>
  );
};

export default Login;