const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

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
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: buildHeaders(options.headers, options.isFormUrlEncoded),
  });

  if (response.status === 204) {
    return null;
  }

  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    throw new Error(payload?.detail || payload || "Erro ao consultar a API.");
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
