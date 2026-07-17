const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function formatApiError(payload) {
  if (!payload) {
    return "Erro ao consultar a API.";
  }

  if (typeof payload === "string") {
    return payload;
  }

  if (Array.isArray(payload?.detail)) {
    return payload.detail
      .map((item) => {
        if (typeof item === "string") {
          return item;
        }

        const field = Array.isArray(item?.loc) ? item.loc.at(-1) : "campo";
        return `${field}: ${item?.msg || "valor invalido"}`;
      })
      .join(" | ");
  }

  if (typeof payload?.detail === "string") {
    return payload.detail;
  }

  return "Erro ao consultar a API.";
}

function buildHeaders(headers = {}, isFormUrlEncoded = false) {
  const finalHeaders = { ...headers };

  if (!isFormUrlEncoded) {
    finalHeaders["Content-Type"] =
      finalHeaders["Content-Type"] || "application/json";
  }

  const token = localStorage.getItem("auth_token");
  if (token) {
    finalHeaders.Authorization = `Bearer ${token}`;
  }

  return finalHeaders;
}

async function apiRequest(path, options = {}) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: buildHeaders(options.headers, options.isFormUrlEncoded),
    });
  } catch {
    throw new Error(
      "Nao foi possivel conectar ao backend. Verifique se a API esta em execucao.",
    );
  }

  if (response.status === 204) {
    return null;
  }

  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    if (response.status >= 500 && path === "/usuarios/cadastro") {
      throw new Error(
        "O backend falhou ao concluir o cadastro. Se o perfil for medico, verifique se o backend esta consistente entre os campos crm/crn.",
      );
    }

    if (response.status >= 500 && path.includes("/fluxo/") && path.endsWith("/iniciar")) {
      throw new Error(
        "A triagem nao pode ser iniciada porque o backend nao encontrou a pergunta inicial do fluxo. O atendimento foi criado, mas o banco precisa ter as perguntas e opcoes carregadas.",
      );
    }

    if (response.status >= 500 && path.includes("/fluxo/") && path.endsWith("/reiniciar")) {
      throw new Error(
        "A triagem nao pode ser reiniciada porque o backend nao encontrou a pergunta inicial do fluxo. O atendimento continua salvo.",
      );
    }

    if (response.status >= 500 && path.includes("/fluxo/")) {
      throw new Error(
        "A triagem nao esta configurada corretamente no backend para este ambiente.",
      );
    }

    throw new Error(formatApiError(payload));
  }

  return payload;
}

export async function loginApi({ username, password }) {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);
  formData.append("grant_type", "password");

  return apiRequest("/usuarios/login", {
    method: "POST",
    body: formData,
    isFormUrlEncoded: true,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
}

export async function getCurrentUser() {
  return apiRequest("/usuarios/me", {
    method: "GET",
  });
}

export async function registerUser(payload) {
  return apiRequest("/usuarios/cadastro", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function createAtendimento(payload) {
  return apiRequest("/atendimentos/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getAtendimento(atendimentoId) {
  return apiRequest(`/atendimentos/${atendimentoId}`, {
    method: "GET",
  });
}

export async function startTriagem(atendimentoId) {
  return apiRequest(`/fluxo/${atendimentoId}/iniciar`, {
    method: "POST",
  });
}

export async function answerTriagem(atendimentoId, payload) {
  return apiRequest(`/fluxo/${atendimentoId}/responder`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function restartTriagem(atendimentoId) {
  return apiRequest(`/fluxo/${atendimentoId}/reiniciar`, {
    method: "DELETE",
  });
}

export async function getTriagemResult(atendimentoId) {
  return apiRequest(`/fluxo/${atendimentoId}/resultado`, {
    method: "GET",
  });
}

export function parseTokenPayload(token) {
  if (!token) {
    return null;
  }

  try {
    const [, payload] = token.split(".");
    if (!payload) {
      return null;
    }

    const normalized = payload.replace(/-/g, "+").replace(/_/g, "/");
    const decoded = atob(normalized);
    return JSON.parse(decoded);
  } catch {
    return null;
  }
}
