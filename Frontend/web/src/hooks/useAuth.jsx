const useAuth = () => {
  const token = localStorage.getItem("accessToken");
  const refreshToken = localStorage.getItem("refreshToken");

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

  const hasRole = (...roles) => {
    return roles.includes(user?.role);
  };

  const hasPermission = (permission) => {
    return user?.permissions?.includes(permission);
  };

  return {
    user,
    token,
    refreshToken,
    role: user?.role,
    isAuthenticated: Boolean(token),
    login,
    logout,
    hasRole,
    hasPermission,
  };
};

export default useAuth;
