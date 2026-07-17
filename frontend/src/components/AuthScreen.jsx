import { useState } from "react";
import { loginApi, parseTokenPayload, registerUser } from "../services/api";
import "./AuthScreen.css";

const roles = [
  { id: "paciente", label: "Paciente" },
  { id: "medico", label: "Medico" },
];

function onlyDigits(value) {
  return value.replace(/\D/g, "");
}

function readStoredProfiles() {
  try {
    const raw = localStorage.getItem("auth_profiles");
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function persistStoredProfile(profile) {
  if (!profile?.cpf) {
    return;
  }

  const profiles = readStoredProfiles();
  profiles[profile.cpf] = {
    cpf: profile.cpf,
    nome: profile.nome || "",
    email: profile.email || null,
    role: profile.role || null,
  };
  localStorage.setItem("auth_profiles", JSON.stringify(profiles));
}

export default function AuthScreen({ onLogin }) {
  const [mode, setMode] = useState("login");
  const [selectedRole, setSelectedRole] = useState("paciente");
  const [cpf, setCpf] = useState("");
  const [password, setPassword] = useState("");
  const [registerForm, setRegisterForm] = useState({
    nome: "",
    email: "",
    telefone: "",
    cpf: "",
    senha: "",
    clinicaId: "",
    idade: "",
    crm: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  function updateRegisterField(field, value) {
    setRegisterForm((current) => ({
      ...current,
      [field]: value,
    }));
  }

  function switchMode(nextMode) {
    setMode(nextMode);
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
        username: onlyDigits(cpf),
        password,
      });

      const tokenPayload = parseTokenPayload(loginResponse.access_token);

      if (!tokenPayload?.sub) {
        throw new Error("Token de autenticacao invalido.");
      }

      const normalizedCpf = onlyDigits(cpf);
      const storedProfiles = readStoredProfiles();
      const storedProfile = storedProfiles[normalizedCpf] || {};

      onLogin(selectedRole, loginResponse.access_token, {
        id: Number(tokenPayload.sub),
        cpf: normalizedCpf,
        nome: storedProfile.nome || `Usuario ${selectedRole}`,
        email: storedProfile.email || null,
        role: storedProfile.role || selectedRole,
      });
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
        telefone: onlyDigits(registerForm.telefone),
        cpf: onlyDigits(registerForm.cpf),
        senha: registerForm.senha,
        role: selectedRole,
        clinica_id: Number(registerForm.clinicaId),
      };

      if (selectedRole === "paciente") {
        payload.idade = Number(registerForm.idade);
      } else {
        payload.crm = registerForm.crm;
      }

      const registeredUser = await registerUser(payload);

      persistStoredProfile({
        cpf: payload.cpf,
        nome: registeredUser?.nome || payload.nome,
        email: registeredUser?.email || payload.email || null,
        role: registeredUser?.role || payload.role,
      });

      setCpf(payload.cpf);
      setPassword(payload.senha);
      setSuccess("Cadastro realizado com sucesso. Agora voce pode entrar.");
      setRegisterForm({
        nome: "",
        email: "",
        telefone: "",
        cpf: "",
        senha: "",
        clinicaId: "",
        idade: "",
        crm: "",
      });
      setMode("login");
    } catch (submitError) {
      setError(submitError.message || "Nao foi possivel concluir o cadastro.");
    } finally {
      setLoading(false);
    }
  }

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
            <p className="auth-hello">
              {mode === "login" ? "Bem-vindo!" : "Criar conta"}
            </p>
            <p className="auth-subtitle">
              {mode === "login"
                ? "Entre com suas credenciais para continuar."
                : "Cadastre um perfil usando os campos aceitos pela API atual."}
            </p>
          </div>

          <div className="auth-mode-toggle" role="tablist">
            <button
              type="button"
              className={`auth-mode ${mode === "login" ? "active" : ""}`}
              onClick={() => switchMode("login")}
            >
              Entrar
            </button>
            <button
              type="button"
              className={`auth-mode ${mode === "register" ? "active" : ""}`}
              onClick={() => switchMode("register")}
            >
              Cadastro
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

          {mode === "login" ? (
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
                {loading ? "Entrando..." : "Entrar"}
              </button>
            </form>
          ) : (
            <form className="auth-form" onSubmit={handleRegisterSubmit}>
              <div className="auth-grid">
                <label className="auth-field">
                  <span>Nome</span>
                  <input
                    type="text"
                    value={registerForm.nome}
                    onChange={(event) => updateRegisterField("nome", event.target.value)}
                    required
                  />
                </label>

                <label className="auth-field">
                  <span>Email</span>
                  <input
                    type="email"
                    value={registerForm.email}
                    onChange={(event) => updateRegisterField("email", event.target.value)}
                  />
                </label>

                <label className="auth-field">
                  <span>Telefone</span>
                  <input
                    type="text"
                    value={registerForm.telefone}
                    onChange={(event) => updateRegisterField("telefone", event.target.value)}
                    required
                  />
                </label>

                <label className="auth-field">
                  <span>CPF</span>
                  <input
                    type="text"
                    value={registerForm.cpf}
                    onChange={(event) => updateRegisterField("cpf", event.target.value)}
                    required
                  />
                </label>

                <label className="auth-field">
                  <span>Senha</span>
                  <input
                    type="password"
                    value={registerForm.senha}
                    onChange={(event) => updateRegisterField("senha", event.target.value)}
                    required
                  />
                </label>

                <label className="auth-field">
                  <span>ID da clinica</span>
                  <input
                    type="number"
                    min="1"
                    value={registerForm.clinicaId}
                    onChange={(event) => updateRegisterField("clinicaId", event.target.value)}
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
                      onChange={(event) => updateRegisterField("idade", event.target.value)}
                      required
                    />
                  </label>
                ) : (
                  <label className="auth-field">
                    <span>CRM</span>
                    <input
                      type="text"
                      value={registerForm.crm}
                      onChange={(event) => updateRegisterField("crm", event.target.value)}
                      required
                    />
                  </label>
                )}
              </div>

              {error ? <p className="auth-error">{error}</p> : null}
              {success ? <p className="auth-success">{success}</p> : null}

              <button type="submit" className="auth-submit" disabled={loading}>
                {loading ? "Cadastrando..." : "Cadastrar"}
              </button>
            </form>
          )}

          <div className="auth-footer auth-footer--actions">
            <button type="button" className="auth-link" onClick={() => switchMode("register")}>
              Criar conta
            </button>
            <span className="auth-note">
              Recuperacao de senha indisponivel na API atual.
            </span>
          </div>
        </div>
      </section>
    </main>
  );
}
