import { useEffect, useState } from "react";
import AuthScreen from "./components/AuthScreen";
import Dashboard from "./components/Dashboard";
import { getCurrentUser } from "./services/api";
import "./App.css";

function App() {
  const [userRole, setUserRole] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("auth_token");

    if (!token) {
      setLoading(false);
      return;
    }

    getCurrentUser()
      .then((currentUser) => {
        setUserRole(currentUser.role);
        setUser(currentUser);
      })
      .catch(() => {
        localStorage.removeItem("auth_token");
        setUserRole(null);
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const handleLogin = (role, token, currentUser) => {
    localStorage.setItem("auth_token", token);
    setUserRole(role);
    setUser(currentUser || null);
  };

  const handleLogout = () => {
    localStorage.removeItem("auth_token");
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
