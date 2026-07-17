import { useState } from "react";
import {
  answerTriagem,
  createAtendimento,
  getAtendimento,
  restartTriagem,
  startTriagem,
} from "../services/api";
import "./Dashboard.css";

function formatDate(dateValue) {
  if (!dateValue) {
    return "--";
  }

  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(dateValue));
}

function statusLabel(status) {
  const labels = {
    aguardando: "Aguardando",
    aguardando_triagem: "Aguardando triagem",
    aguardando_atendimento: "Aguardando atendimento",
    em_atendimento: "Em atendimento",
    finalizado: "Finalizado",
  };

  return labels[status] || status || "--";
}

function riscoLabel(classificacao) {
  const labels = {
    baixo: "Baixo",
    medio: "Medio",
    alto: "Alto",
  };

  return labels[classificacao] || classificacao || "--";
}

function triagemLabel(classificacao) {
  return classificacao ? classificacao.replaceAll("_", " ") : "--";
}

function triagemStatusLabel(atendimento, triagemFinalizada, currentQuestion) {
  if (currentQuestion) {
    return "Em andamento";
  }

  if (triagemFinalizada) {
    return "Concluida";
  }

  if (atendimento?.status === "aguardando_triagem") {
    return "Pendente";
  }

  if (atendimento?.classificacao_triagem) {
    return "Concluida";
  }

  return "Aguardando";
}

export default function Dashboard({ role, user, onLogout }) {
  const [clinicaId, setClinicaId] = useState("");
  const [atendimentoId, setAtendimentoId] = useState("");
  const [atendimento, setAtendimento] = useState(null);
  const [triagem, setTriagem] = useState(null);
  const [selectedOptionId, setSelectedOptionId] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loadingAction, setLoadingAction] = useState(false);
  const [triagemIndisponivel, setTriagemIndisponivel] = useState(false);

  const currentQuestion = triagem?.proxima_pergunta;
  const triagemFinalizada = triagem?.concluido;
  const ocultarResultadoPersistido =
    role === "paciente" && triagem && !triagemFinalizada;
  const classificacaoTriagemExibida = ocultarResultadoPersistido
    ? null
    : atendimento?.classificacao_triagem || triagem?.resultado?.classificacao_triagem;
  const classificacaoRiscoExibida = ocultarResultadoPersistido
    ? null
    : atendimento?.classificacao_risco;
  const resumoIaExibido = ocultarResultadoPersistido ? null : atendimento?.resumo_ia;

  async function refreshAtendimentoState(targetAtendimentoId) {
    const atendimentoAtualizado = await getAtendimento(targetAtendimentoId);
    setAtendimento(atendimentoAtualizado);
    return atendimentoAtualizado;
  }

  async function handleCreateAtendimento(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    setLoadingAction(true);
    setTriagemIndisponivel(false);

    try {
      const created = await createAtendimento({
        clinica_id: Number(clinicaId),
        paciente_id: user.id,
      });

      setAtendimento(created);
      setAtendimentoId(String(created.id));
      setMessage(`Atendimento #${created.id} criado com sucesso.`);

      try {
        const fluxo = await startTriagem(created.id);
        setTriagem(fluxo);
        setSelectedOptionId("");
        setMessage(`Atendimento #${created.id} criado e triagem iniciada.`);
      } catch (triagemError) {
        setTriagem(null);
        setTriagemIndisponivel(true);
        setError(triagemError.message);
      }
    } catch (requestError) {
      setError(requestError.message || "Nao foi possivel criar o atendimento.");
    } finally {
      setLoadingAction(false);
    }
  }

  async function handleAnswerQuestion(event) {
    event.preventDefault();

    if (!currentQuestion || !selectedOptionId || !atendimento?.id) {
      return;
    }

    setError("");
    setMessage("");
    setLoadingAction(true);
    setTriagemIndisponivel(false);

    try {
      const fluxo = await answerTriagem(atendimento.id, {
        pergunta_id: currentQuestion.id,
        opcao_resposta_id: Number(selectedOptionId),
      });

      setTriagem(fluxo);
      setSelectedOptionId("");

      if (fluxo.concluido) {
        await refreshAtendimentoState(atendimento.id);
        setMessage("Triagem concluida com sucesso.");
      }
    } catch (requestError) {
      setError(requestError.message || "Nao foi possivel enviar a resposta.");
    } finally {
      setLoadingAction(false);
    }
  }

  async function handleRestartTriagem() {
    if (!atendimento?.id) {
      return;
    }

    setError("");
    setMessage("");
    setLoadingAction(true);
    setTriagemIndisponivel(false);

    try {
      const fluxo = await restartTriagem(atendimento.id);
      await refreshAtendimentoState(atendimento.id);
      setTriagem(fluxo);
      setSelectedOptionId("");
      setMessage("Triagem reiniciada.");
    } catch (requestError) {
      setTriagemIndisponivel(true);
      setError(requestError.message || "Nao foi possivel reiniciar a triagem.");
    } finally {
      setLoadingAction(false);
    }
  }

  async function handleBuscarAtendimento(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    setLoadingAction(true);
    setTriagemIndisponivel(false);

    try {
      await refreshAtendimentoState(Number(atendimentoId));
      setTriagem(null);

      setMessage(`Atendimento #${atendimentoId} carregado.`);
    } catch (requestError) {
      setError(
        requestError.message || "Nao foi possivel buscar o atendimento.",
      );
    } finally {
      setLoadingAction(false);
    }
  }

  return (
    <main className="dashboard-page">
      <div className="dashboard-topbar">
        <div>
          <p className="dashboard-welcome">Bem-vindo de volta</p>
          <h1>
            {role === "medico"
              ? "Consulta de atendimentos"
              : "Fluxo de triagem"}
          </h1>
        </div>

        <div className="dashboard-user">
          <div>
            <p>{role === "medico" ? "Medico" : "Paciente"} conectado</p>
            <strong>{user?.nome || "Usuario"}</strong>
          </div>
          <button className="dashboard-logout" onClick={onLogout}>
            Sair
          </button>
        </div>
      </div>

      <section className="dashboard-grid">
        <aside className="dashboard-summary">
          <div className="summary-card summary-card--focus">
            <p className="summary-label">Usuario autenticado</p>
            <strong>{user?.cpf || "--"}</strong>
            <p className="summary-note">
              Os dados desta tela agora sao carregados e enviados para a API do
              backend.
            </p>
          </div>

          <div className="summary-card">
            <div>
              <p className="summary-label">Perfil</p>
              <strong>{role === "medico" ? "Medico" : "Paciente"}</strong>
            </div>
            <p className="summary-note">
              Email: {user?.email || "nao informado"}
            </p>
          </div>

          <div className="summary-card">
            <div>
              <p className="summary-label">Atendimento atual</p>
              <strong>{atendimento ? `#${atendimento.id}` : "--"}</strong>
            </div>
            <p className="summary-note">
              Status: {statusLabel(atendimento?.status)}
            </p>
          </div>
        </aside>

        <section className="dashboard-main">
          <div className="dashboard-cards">
            <article className="dashboard-card">
              <p>{role === "medico" ? "ID do atendimento" : "ID do usuario"}</p>
              <strong>{role === "medico" ? atendimento?.id || "--" : user?.id || "--"}</strong>
            </article>
            <article className="dashboard-card">
              <p>{role === "medico" ? "Classificacao da triagem" : "Risco do atendimento"}</p>
              <strong>
                {role === "medico"
                  ? triagemLabel(classificacaoTriagemExibida)
                  : riscoLabel(classificacaoRiscoExibida)}
              </strong>
            </article>
            <article className="dashboard-card">
              <p>{role === "medico" ? "Risco persistido" : "Triagem"}</p>
              <strong>{riscoLabel(classificacaoRiscoExibida)}</strong>
              {role !== "medico" ? (
                <strong>
                  {triagemStatusLabel(atendimento, triagemFinalizada, currentQuestion)}
                </strong>
              ) : null}
            </article>
          </div>

          <div className="dashboard-panel">
            <div className="panel-header">
              <div>
                <span>
                  {role === "medico"
                    ? "Buscar atendimento"
                    : "Novo atendimento"}
                </span>
                <h2>
                  {role === "medico"
                    ? "Consultar dados reais da API"
                    : "Criar atendimento e iniciar triagem"}
                </h2>
              </div>
            </div>

            <div className="panel-body">
              {role === "paciente" ? (
                <form
                  className="dashboard-form"
                  onSubmit={handleCreateAtendimento}
                >
                  <label className="dashboard-field">
                    <span>ID da clinica</span>
                    <input
                      type="number"
                      min="1"
                      placeholder="Informe a clinica do paciente"
                      value={clinicaId}
                      onChange={(event) => setClinicaId(event.target.value)}
                      required
                    />
                  </label>
                  <button type="submit" disabled={loadingAction}>
                    {loadingAction ? "Processando..." : "Criar atendimento"}
                  </button>
                </form>
              ) : (
                <form
                  className="dashboard-form"
                  onSubmit={handleBuscarAtendimento}
                >
                  <label className="dashboard-field">
                    <span>ID do atendimento</span>
                    <input
                      type="number"
                      min="1"
                      placeholder="Digite o atendimento"
                      value={atendimentoId}
                      onChange={(event) => setAtendimentoId(event.target.value)}
                      required
                    />
                  </label>
                  <button type="submit" disabled={loadingAction}>
                    {loadingAction ? "Buscando..." : "Buscar atendimento"}
                  </button>
                </form>
              )}

              {message ? (
                <p className="dashboard-feedback dashboard-feedback--success">
                  {message}
                </p>
              ) : null}
              {error ? (
                <p className="dashboard-feedback dashboard-feedback--error">
                  {error}
                </p>
              ) : null}
            </div>
          </div>

          <div className="dashboard-table-card">
            <div className="table-header">
              <div>
                <p>
                  {role === "medico"
                    ? "Atendimento consultado"
                    : "Etapa atual da triagem"}
                </p>
                <strong>
                  {role === "medico"
                    ? "Dados do backend"
                    : "Perguntas e resultado"}
                </strong>
              </div>
              {role === "paciente" && atendimento ? (
                <button onClick={handleRestartTriagem} disabled={loadingAction}>
                  Reiniciar triagem
                </button>
              ) : null}
            </div>

            {atendimento ? (
              <div className="protocol-table">
                <div className="protocol-row protocol-row--head">
                  <span>ID</span>
                  <span>Status</span>
                  <span>Risco</span>
                  <span>Data</span>
                </div>
                <div className="protocol-row">
                  <span>#{atendimento.id}</span>
                  <span>{statusLabel(atendimento.status)}</span>
                  <span>{riscoLabel(classificacaoRiscoExibida)}</span>
                  <span>{formatDate(atendimento.data_atendimento)}</span>
                </div>
              </div>
            ) : (
              <p className="empty-state">Nenhum atendimento carregado ainda.</p>
            )}

            {role === "medico" && atendimento ? (
              <div className="triagem-result">
                <p className="triagem-step">Leitura clinica do atendimento</p>
                <span>Classificacao da triagem: {triagemLabel(classificacaoTriagemExibida)}</span>
                <span>Paciente: #{atendimento.paciente_id || "--"}</span>
                <span>Medico vinculado: {atendimento.medico_id ? `#${atendimento.medico_id}` : "Nao vinculado"}</span>
              </div>
            ) : null}

            {resumoIaExibido ? (
              <div className="triagem-result">
                <p className="triagem-step">Resumo salvo no atendimento</p>
                <span>{resumoIaExibido}</span>
              </div>
            ) : null}

            {role === "paciente" &&
            atendimento &&
            triagemIndisponivel &&
            !currentQuestion &&
            !triagemFinalizada ? (
              <div className="triagem-result">
                <p className="triagem-step">Triagem indisponivel neste ambiente</p>
                <span>
                  O atendimento foi criado, mas o backend nao encontrou a pergunta
                  inicial do fluxo para abrir a triagem.
                </span>
              </div>
            ) : null}

            {role === "paciente" && currentQuestion ? (
              <form className="triagem-card" onSubmit={handleAnswerQuestion}>
                <div>
                  <p className="triagem-step">Pergunta #{currentQuestion.id}</p>
                  <h3>{currentQuestion.texto}</h3>
                </div>

                <div className="triagem-options">
                  {currentQuestion.opcoes.map((opcao) => (
                    <label key={opcao.id} className="triagem-option">
                      <input
                        type="radio"
                        name="triagem_opcao"
                        value={opcao.id}
                        checked={selectedOptionId === String(opcao.id)}
                        onChange={(event) =>
                          setSelectedOptionId(event.target.value)
                        }
                      />
                      <span>{opcao.texto}</span>
                    </label>
                  ))}
                </div>

                <button
                  type="submit"
                  disabled={loadingAction || !selectedOptionId}
                >
                  {loadingAction ? "Enviando..." : "Responder"}
                </button>
              </form>
            ) : null}

            {triagemFinalizada && triagem?.resultado ? (
              <div className="triagem-result">
                <p className="triagem-step">Resultado da triagem</p>
                <h3>{triagemLabel(triagem.resultado.classificacao_triagem)}</h3>
                <span>
                  Pontuacao total: {triagem.resultado.pontuacao_total}
                </span>
              </div>
            ) : null}
          </div>
        </section>
      </section>
    </main>
  );
}
