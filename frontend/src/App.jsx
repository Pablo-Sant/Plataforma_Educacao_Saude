import { useEffect, useState } from "react";
import AuthScreen from "./components/AuthScreen";
import Dashboard from "./components/Dashboard";
import { parseTokenPayload } from "./services/api";
import "./App.css";

function readStoredProfiles() {
  try {
    const raw = localStorage.getItem("auth_profiles");
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function App() {
  const [userRole, setUserRole] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("auth_token");
    const session = localStorage.getItem("auth_session");

    if (!token) {
      setLoading(false);
      return;
    }

    const payload = parseTokenPayload(token);

    if (!payload?.sub) {
      localStorage.removeItem("auth_token");
      localStorage.removeItem("auth_session");
      setLoading(false);
      return;
    }

    const persistedSession = session ? JSON.parse(session) : {};
    const storedProfiles = readStoredProfiles();
    const storedProfile = persistedSession.cpf
      ? storedProfiles[persistedSession.cpf] || {}
      : {};
    const restoredUser = {
      id: Number(payload.sub),
      cpf: persistedSession.cpf || storedProfile.cpf || "",
      nome: persistedSession.nome || storedProfile.nome || "Usuario",
      email: persistedSession.email || storedProfile.email || null,
      role: persistedSession.role || storedProfile.role || null,
    };

    setUserRole(restoredUser.role);
    setUser(restoredUser);
    setLoading(false);
  }, []);

  const handleLogin = (role, token, currentUser) => {
    localStorage.setItem("auth_token", token);
    localStorage.setItem("auth_session", JSON.stringify(currentUser || {}));
    setUserRole(role);
    setUser(currentUser || null);
  };

  const handleLogout = () => {
    localStorage.removeItem("auth_token");
    localStorage.removeItem("auth_session");
    setUserRole(null);
    setUser(null);
  };

  if (loading) {
    return <div className="app-loading">Carregando...</div>;
  }

  return userRole ? (
    <Dashboard role={userRole} user={user} onLogout={handleLogout} />
  ) : (
    <AuthScreen onLogin={handleLogin} />
  );
}

export default App;
