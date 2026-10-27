import { BrowserRouter, Navigate, Outlet, Route, Routes } from "react-router";
import { AuthProvider, useAuth } from "./auth.jsx";
import Layout from "./components/Layout.jsx";
import { Spinner } from "./components/ui.jsx";
import GroupDetail from "./pages/GroupDetail.jsx";
import Groups from "./pages/Groups.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";

// Pages inside this need a logged-in user; everyone else is sent to /login.
function RequireAuth() {
  const { token, loading } = useAuth();
  if (!token) return <Navigate to="/login" replace />;
  if (loading) return <Spinner />;
  return (
    <Layout>
      <Outlet />
    </Layout>
  );
}

// Login/register pages make no sense when you're already logged in.
function GuestOnly() {
  const { token } = useAuth();
  return token ? <Navigate to="/" replace /> : <Outlet />;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<GuestOnly />}>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Route>
          <Route element={<RequireAuth />}>
            <Route path="/" element={<Groups />} />
            <Route path="/groups/:groupId" element={<GroupDetail />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
