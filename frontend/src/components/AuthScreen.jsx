import { useState } from "react";
import { loginApi, getCurrentUser } from "../services/api";
import "./AuthScreen.css";

const roles = [
  { id: "paciente", label: "Paciente" },
  { id: "medico", label: "Médico" },
];

export default function AuthScreen({ onLogin }) {
  const [selectedRole, setSelectedRole] = useState("paciente");
  const [cpf, setCpf] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const loginResponse = await loginApi({
        username: cpf,
        password,
      });

      localStorage.setItem("auth_token", loginResponse.access_token);

      const user = await getCurrentUser();
      const role = user.role;

      if (selectedRole !== role) {
        throw new Error(
          "Perfil selecionado não corresponde ao usuário autenticado.",
        );
      }

      onLogin(role, loginResponse.access_token, user);
    } catch (submitError) {
      setError(submitError.message || "Não foi possível autenticar.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <section className="auth-card">
        <div className="auth-panel auth-panel--info">
          <div className="auth-brand">
            <span className="auth-brand__tag">Sistema de Protocolos</span>
            <h1 className="auth-brand__title">Gestão de informações</h1>
          </div>

          <p className="auth-copy">
            Para Pacientes
            <span>
              Realize sua triagem de sintomas de forma rápida e receba
              orientações personalizadas sobre sua condição.
            </span>
          </p>

          <p className="auth-copy">
            Para Médicos
            <span>
              Acesse relatórios completos de triagem, visualize protocolos
              sugeridos e gerencie atendimentos com eficiência.
            </span>
          </p>

          <div className="auth-steps">
            <div>
              <strong>+1000</strong>
              <small>protocolos ativos</small>
            </div>
            <div>
              <strong>3 minutos</strong>
              <small>para começar</small>
            </div>
          </div>
        </div>

        <div className="auth-panel auth-panel--form">
          <div className="auth-header">
            <p className="auth-hello">Bem-vindo!</p>
            <p className="auth-subtitle">
              Entre com suas credenciais para continuar.
            </p>
          </div>

          <div className="auth-role-toggle" role="tablist">
            {roles.map((role) => (
              <button
                key={role.id}
                type="button"
                className={`auth-role ${selectedRole === role.id ? "active" : ""}`}
                onClick={() => setSelectedRole(role.id)}
                aria-selected={selectedRole === role.id}
              >
                {role.label}
              </button>
            ))}
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            <label className="auth-field">
              <span>CPF</span>
              <input
                type="text"
                placeholder="00000000000"
                value={cpf}
                onChange={(event) => setCpf(event.target.value)}
              />
            </label>

            <label className="auth-field">
              <span>Senha</span>
              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
            </label>

            {error ? <p className="auth-error">{error}</p> : null}

            <button type="submit" className="auth-submit" disabled={loading}>
              {loading ? "Entrando..." : "Entrar"}
            </button>
          </form>

          <div className="auth-footer">
            <p>Ainda não é cadastrado?</p>
            <a href="#register">Criar conta</a>
          </div>

          <div className="auth-help">
            <span>Esqueceu sua senha?</span>
            <a href="#recover">Recuperar agora</a>
          </div>
        </div>
      </section>
    </main>
  );
}
