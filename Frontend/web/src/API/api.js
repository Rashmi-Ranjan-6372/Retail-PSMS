import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8001/api",
});

// ---------------- REQUEST INTERCEPTOR ---------------- //
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("accessToken");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// ---------------- RESPONSE INTERCEPTOR ---------------- //

let isRefreshing = false;
let refreshSubscribers = [];

const subscribeTokenRefresh = (cb) => {
  refreshSubscribers.push(cb);
};

const onRefreshed = (token) => {
  refreshSubscribers.forEach((cb) => cb(token));
  refreshSubscribers = [];
};

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve) => {
          subscribeTokenRefresh((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            resolve(api(originalRequest));
          });
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const refresh = localStorage.getItem("refreshToken");

        const res = await axios.post(
          "http://127.0.0.1:8001/api/token/refresh/",
          { refresh }
        );

        const newAccess = res.data.access;
        const newRefresh = res.data.refresh;

        // 🔥 update tokens
        localStorage.setItem("accessToken", newAccess);
        localStorage.setItem("refreshToken", newRefresh);

        api.defaults.headers.Authorization = `Bearer ${newAccess}`;

        onRefreshed(newAccess);

        return api(originalRequest);
      } catch (err) {
        localStorage.clear();
        window.location.href = "/login";
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;