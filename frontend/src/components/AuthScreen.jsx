import { useState } from "react";
import {
  getCurrentUser,
  loginApi,
  recoverPassword,
  registerUser,
} from "../services/api";
import "./AuthScreen.css";

const roles = [
  { id: "paciente", label: "Paciente" },
  { id: "medico", label: "Medico" },
];

const authModes = {
  login: {
    title: "Bem-vindo!",
    subtitle: "Entre com suas credenciais para continuar.",
    submitLabel: "Entrar",
  },
  register: {
    title: "Criar conta",
    subtitle: "Cadastre um perfil para acessar a plataforma.",
    submitLabel: "Cadastrar",
  },
  recover: {
    title: "Recuperar senha",
    subtitle: "Confirme seus dados para definir uma nova senha.",
    submitLabel: "Atualizar senha",
  },
};

function emptyRegisterForm(role) {
  return {
    nome: "",
    email: "",
    telefone: "",
    cpf: "",
    senha: "",
    clinicaId: "",
    idade: role === "paciente" ? "" : "",
    crm: role === "medico" ? "" : "",
  };
}

export default function AuthScreen({ onLogin }) {
  const [authMode, setAuthMode] = useState("login");
  const [selectedRole, setSelectedRole] = useState("paciente");
  const [cpf, setCpf] = useState("");
  const [password, setPassword] = useState("");
  const [registerForm, setRegisterForm] = useState(emptyRegisterForm("paciente"));
  const [recoverForm, setRecoverForm] = useState({
    cpf: "",
    email: "",
    novaSenha: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  function switchMode(mode) {
    setAuthMode(mode);
    setError("");
    setSuccess("");
  }

  function handleRoleChange(role) {
    setSelectedRole(role);
    setRegisterForm((current) => ({
      ...current,
      idade: role === "paciente" ? current.idade : "",
      crm: role === "medico" ? current.crm : "",
    }));
  }

  async function handleLoginSubmit(event) {
    event.preventDefault();
    setError("");
    setSuccess("");
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
        throw new Error("Perfil selecionado nao corresponde ao usuario autenticado.");
      }

      onLogin(role, loginResponse.access_token, user);
    } catch (submitError) {
      setError(submitError.message || "Nao foi possivel autenticar.");
    } finally {
      setLoading(false);
    }
  }

  async function handleRegisterSubmit(event) {
    event.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const payload = {
        nome: registerForm.nome,
        email: registerForm.email || null,
        telefone: registerForm.telefone,
        cpf: registerForm.cpf,
        senha: registerForm.senha,
        role: selectedRole,
        clinica_id: Number(registerForm.clinicaId),
      };

      if (selectedRole === "paciente") {
        payload.idade = Number(registerForm.idade);
      } else {
        payload.crm = registerForm.crm;
      }

      await registerUser(payload);
      setSuccess("Cadastro realizado com sucesso. Agora voce ja pode entrar.");
      setRegisterForm(emptyRegisterForm(selectedRole));
      setCpf(payload.cpf);
      setPassword(payload.senha);
      setAuthMode("login");
    } catch (submitError) {
      setError(submitError.message || "Nao foi possivel concluir o cadastro.");
    } finally {
      setLoading(false);
    }
  }

  async function handleRecoverSubmit(event) {
    event.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      await recoverPassword({
        cpf: recoverForm.cpf,
        email: recoverForm.email,
        nova_senha: recoverForm.novaSenha,
      });

      setSuccess("Senha atualizada com sucesso. Voce ja pode entrar com a nova senha.");
      setCpf(recoverForm.cpf);
      setPassword(recoverForm.novaSenha);
      setRecoverForm({
        cpf: "",
        email: "",
        novaSenha: "",
      });
      setAuthMode("login");
    } catch (submitError) {
      setError(submitError.message || "Nao foi possivel atualizar a senha.");
    } finally {
      setLoading(false);
    }
  }

  const modeContent = authModes[authMode];

  return (
    <main className="auth-page">
      <section className="auth-card">
        <div className="auth-panel auth-panel--info">
          <div className="auth-brand">
            <span className="auth-brand__tag">Sistema de Protocolos</span>
            <h1 className="auth-brand__title">Gestao de informacoes</h1>
          </div>

          <p className="auth-copy">
            Para Pacientes
            <span>
              Realize sua triagem de sintomas de forma rapida e receba orientacoes
              personalizadas sobre sua condicao.
            </span>
          </p>

          <p className="auth-copy">
            Para Medicos
            <span>
              Acesse relatorios completos de triagem, visualize protocolos
              sugeridos e gerencie atendimentos com eficiencia.
            </span>
          </p>

          <div className="auth-steps">
            <div>
              <strong>+1000</strong>
              <small>protocolos ativos</small>
            </div>
            <div>
              <strong>3 minutos</strong>
              <small>para comecar</small>
            </div>
          </div>
        </div>

        <div className="auth-panel auth-panel--form">
          <div className="auth-header">
            <p className="auth-hello">{modeContent.title}</p>
            <p className="auth-subtitle">{modeContent.subtitle}</p>
          </div>

          <div className="auth-mode-toggle" role="tablist">
            <button
              type="button"
              className={`auth-mode ${authMode === "login" ? "active" : ""}`}
              onClick={() => switchMode("login")}
            >
              Entrar
            </button>
            <button
              type="button"
              className={`auth-mode ${authMode === "register" ? "active" : ""}`}
              onClick={() => switchMode("register")}
            >
              Cadastro
            </button>
            <button
              type="button"
              className={`auth-mode ${authMode === "recover" ? "active" : ""}`}
              onClick={() => switchMode("recover")}
            >
              Recuperar
            </button>
          </div>

          <div className="auth-role-toggle" role="tablist">
            {roles.map((role) => (
              <button
                key={role.id}
                type="button"
                className={`auth-role ${selectedRole === role.id ? "active" : ""}`}
                onClick={() => handleRoleChange(role.id)}
                aria-selected={selectedRole === role.id}
              >
                {role.label}
              </button>
            ))}
          </div>

          {authMode === "login" ? (
            <form className="auth-form" onSubmit={handleLoginSubmit}>
              <label className="auth-field">
                <span>CPF</span>
                <input
                  type="text"
                  placeholder="00000000000"
                  value={cpf}
                  onChange={(event) => setCpf(event.target.value)}
                  required
                />
              </label>

              <label className="auth-field">
                <span>Senha</span>
                <input
                  type="password"
                  placeholder="Digite sua senha"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                />
              </label>

              {error ? <p className="auth-error">{error}</p> : null}
              {success ? <p className="auth-success">{success}</p> : null}

              <button type="submit" className="auth-submit" disabled={loading}>
                {loading ? "Entrando..." : modeContent.submitLabel}
              </button>
            </form>
          ) : null}

          {authMode === "register" ? (
            <form className="auth-form" onSubmit={handleRegisterSubmit}>
              <div className="auth-grid">
                <label className="auth-field">
                  <span>Nome</span>
                  <input
                    type="text"
                    value={registerForm.nome}
                    onChange={(event) =>
                      setRegisterForm((current) => ({
                        ...current,
                        nome: event.target.value,
                      }))
                    }
                    required
                  />
                </label>

                <label className="auth-field">
                  <span>Email</span>
                  <input
                    type="email"
                    value={registerForm.email}
                    onChange={(event) =>
                      setRegisterForm((current) => ({
                        ...current,
                        email: event.target.value,
                      }))
                    }
                    required
                  />
                </label>

                <label className="auth-field">
                  <span>Telefone</span>
                  <input
                    type="text"
                    value={registerForm.telefone}
                    onChange={(event) =>
                      setRegisterForm((current) => ({
                        ...current,
                        telefone: event.target.value,
                      }))
                    }
                    required
                  />
                </label>

                <label className="auth-field">
                  <span>CPF</span>
                  <input
                    type="text"
                    value={registerForm.cpf}
                    onChange={(event) =>
                      setRegisterForm((current) => ({
                        ...current,
                        cpf: event.target.value,
                      }))
                    }
                    required
                  />
                </label>

                <label className="auth-field">
                  <span>Senha</span>
                  <input
                    type="password"
                    value={registerForm.senha}
                    onChange={(event) =>
                      setRegisterForm((current) => ({
                        ...current,
                        senha: event.target.value,
                      }))
                    }
                    required
                  />
                </label>

                <label className="auth-field">
                  <span>ID da clinica</span>
                  <input
                    type="number"
                    min="1"
                    value={registerForm.clinicaId}
                    onChange={(event) =>
                      setRegisterForm((current) => ({
                        ...current,
                        clinicaId: event.target.value,
                      }))
                    }
                    required
                  />
                </label>

                {selectedRole === "paciente" ? (
                  <label className="auth-field">
                    <span>Idade</span>
                    <input
                      type="number"
                      min="0"
                      value={registerForm.idade}
                      onChange={(event) =>
                        setRegisterForm((current) => ({
                          ...current,
                          idade: event.target.value,
                        }))
                      }
                      required
                    />
                  </label>
                ) : (
                  <label className="auth-field">
                    <span>CRM</span>
                    <input
                      type="text"
                      value={registerForm.crm}
                      onChange={(event) =>
                        setRegisterForm((current) => ({
                          ...current,
                          crm: event.target.value,
                        }))
                      }
                      required
                    />
                  </label>
                )}
              </div>

              {error ? <p className="auth-error">{error}</p> : null}
              {success ? <p className="auth-success">{success}</p> : null}

              <button type="submit" className="auth-submit" disabled={loading}>
                {loading ? "Cadastrando..." : modeContent.submitLabel}
              </button>
            </form>
          ) : null}

          {authMode === "recover" ? (
            <form className="auth-form" onSubmit={handleRecoverSubmit}>
              <label className="auth-field">
                <span>CPF</span>
                <input
                  type="text"
                  value={recoverForm.cpf}
                  onChange={(event) =>
                    setRecoverForm((current) => ({
                      ...current,
                      cpf: event.target.value,
                    }))
                  }
                  required
                />
              </label>

              <label className="auth-field">
                <span>Email</span>
                <input
                  type="email"
                  value={recoverForm.email}
                  onChange={(event) =>
                    setRecoverForm((current) => ({
                      ...current,
                      email: event.target.value,
                    }))
                  }
                  required
                />
              </label>

              <label className="auth-field">
                <span>Nova senha</span>
                <input
                  type="password"
                  value={recoverForm.novaSenha}
                  onChange={(event) =>
                    setRecoverForm((current) => ({
                      ...current,
                      novaSenha: event.target.value,
                    }))
                  }
                  required
                />
              </label>

              {error ? <p className="auth-error">{error}</p> : null}
              {success ? <p className="auth-success">{success}</p> : null}

              <button type="submit" className="auth-submit" disabled={loading}>
                {loading ? "Atualizando..." : modeContent.submitLabel}
              </button>
            </form>
          ) : null}

          <div className="auth-footer auth-footer--actions">
            <button type="button" className="auth-link" onClick={() => switchMode("register")}>
              Criar conta
            </button>
            <button type="button" className="auth-link" onClick={() => switchMode("recover")}>
              Recuperar senha
            </button>
          </div>
        </div>
      </section>
    </main>
  );
}
