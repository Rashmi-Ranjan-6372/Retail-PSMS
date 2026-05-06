import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "../pages/Auth/Login";
import Dashboard from "../pages/Dashboard/Dashboard";
import ProtectedRoute from "./ProtectedRoute";
import Layout from "../components/Layout";

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />  

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </ProtectedRoute>
          }
        />

        <Route path="*" element={<Login />} />

      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;