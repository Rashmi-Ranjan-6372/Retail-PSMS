const useAuth = () => {
  const token = localStorage.getItem("accessToken");
  const user = JSON.parse(localStorage.getItem("user") || "null");

  const login = (data) => {
    localStorage.setItem("accessToken", data.tokens.access);
    localStorage.setItem("refreshToken", data.tokens.refresh);
    localStorage.setItem("user", JSON.stringify(data.user));
  };

  const logout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("user");
  };

  return {
    user,
    role: user?.role,
    isAuthenticated: !!token,
    login,
    logout,
  };
};

export default useAuth;