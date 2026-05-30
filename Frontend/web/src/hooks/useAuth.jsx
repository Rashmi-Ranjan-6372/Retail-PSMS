const useAuth = () => {
  const login = (data) => {
    const { access, refresh } = data.tokens;

    localStorage.setItem("accessToken", access);
    localStorage.setItem("refreshToken", refresh);
    localStorage.setItem("user", JSON.stringify(data.user));
  };

  const logout = () => {
    localStorage.clear();
  };

  const isAuthenticated = () => {
    return !!localStorage.getItem("accessToken");
  };

  return { login, logout, isAuthenticated };
};

export default useAuth;
