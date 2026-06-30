import { useState, useEffect } from "react";

const useAuth = () => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Load auth state on first render
  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    const storedUser = localStorage.getItem("user");

    if (token && storedUser) {
      try {
        setUser(JSON.parse(storedUser));
        setIsAuthenticated(true);
      } catch (err) {
        console.error("Invalid user data in localStorage");
        localStorage.clear();
        setUser(null);
        setIsAuthenticated(false);
      }
    } else {
      setUser(null);
      setIsAuthenticated(false);
    }
  }, []);

  // Login
  const login = (data) => {
    const { access, refresh } = data.tokens;

    localStorage.setItem("accessToken", access);
    localStorage.setItem("refreshToken", refresh);
    localStorage.setItem("user", JSON.stringify(data.user));

    setUser(data.user);
    setIsAuthenticated(true);
  };

  // Logout
  const logout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("user");

    setUser(null);
    setIsAuthenticated(false);
  };

  return {
    user,
    role: user?.role,
    login,
    logout,
    isAuthenticated,
  };
};

export default useAuth;