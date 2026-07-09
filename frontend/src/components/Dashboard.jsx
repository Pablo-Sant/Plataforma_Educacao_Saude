import "./Dashboard.css";

const protocolList = [
  {
    id: "#P-5821",
    title: "Triagem de paciente com dor crônica",
    status: "Em análise",
    level: "Prioridade média",
    due: "Hoje, 16:30",
    owner: "Dr. Mariana Silva",
  },
  {
    id: "#P-5822",
    title: "Protocolo pós-operatório de joelho",
    status: "Aguardando revisão",
    level: "Alta prioridade",
    due: "Amanhã, 09:00",
    owner: "Dr. Felipe Costa",
  },
  {
    id: "#P-5823",
    title: "Avaliação de sintomas respiratórios",
    status: "Concluído",
    level: "Normal",
    due: "Ontem, 18:45",
    owner: "Dra. Ana Lins",
  },
];

const stats = [
  { label: "Protocolos ativos", value: "128" },
  { label: "Atendimentos hoje", value: "24" },
  { label: "Relatórios gerados", value: "84" },
];

export default function Dashboard({ role, onLogout }) {
  return (
    <main className="dashboard-page">
      <div className="dashboard-topbar">
        <div>
          <p className="dashboard-welcome">Bem-vindo de volta</p>
          <h1>Visão geral do protocolo</h1>
        </div>

        <div className="dashboard-user">
          <div>
            <p>{role === "medico" ? "Médico" : "Paciente"} conectado</p>
            <strong>
              {role === "medico" ? "Dr. Felipe" : "Paciente João"}
            </strong>
          </div>
          <button className="dashboard-logout" onClick={onLogout}>
            Sair
          </button>
        </div>
      </div>

      <section className="dashboard-grid">
        <aside className="dashboard-summary">
          <div className="summary-card summary-card--focus">
            <p className="summary-label">Protocolo ativo</p>
            <strong>#P-5821</strong>
            <p className="summary-note">
              Diagnóstico inicial e plano de tratamento em andamento.
            </p>
          </div>

          <div className="summary-card">
            <div>
              <p className="summary-label">Próximo atendimento</p>
              <strong>16:30</strong>
            </div>
            <p className="summary-note">
              Sessão com paciente em recuperação pós-operatória.
            </p>
          </div>

          <div className="summary-card">
            <div>
              <p className="summary-label">Última atualização</p>
              <strong>Há 12 minutos</strong>
            </div>
            <p className="summary-note">
              Entrada de dados salva automaticamente.
            </p>
          </div>
        </aside>

        <section className="dashboard-main">
          <div className="dashboard-cards">
            {stats.map((item) => (
              <article key={item.label} className="dashboard-card">
                <p>{item.label}</p>
                <strong>{item.value}</strong>
              </article>
            ))}
          </div>

          <div className="dashboard-panel">
            <div className="panel-header">
              <div>
                <span>Protocolo em destaque</span>
                <h2>Triagem de sintomas respiratórios</h2>
              </div>
              <button>Ver tudo</button>
            </div>
            <div className="panel-body">
              <p className="panel-text">
                Veja os detalhes do protocolo e acompanhe o progresso de cada
                etapa em um fluxo unificado.
              </p>
              <div className="panel-meta">
                <span>Envolvidos: 5 profissionais</span>
                <span>Relatórios: 12</span>
              </div>
            </div>
          </div>

          <div className="dashboard-table-card">
            <div className="table-header">
              <div>
                <p>Protocolos recentes</p>
                <strong>Últimos 3 registros</strong>
              </div>
              <button>Atualizar</button>
            </div>

            <div className="protocol-table">
              <div className="protocol-row protocol-row--head">
                <span>ID</span>
                <span>Protocolo</span>
                <span>Status</span>
                <span>Vencimento</span>
              </div>
              {protocolList.map((protocol) => (
                <div key={protocol.id} className="protocol-row">
                  <span>{protocol.id}</span>
                  <span>{protocol.title}</span>
                  <span
                    className={`protocol-status protocol-status--${protocol.status.replace(/\s+/g, "-").toLowerCase()}`}
                  >
                    {protocol.status}
                  </span>
                  <span>{protocol.due}</span>
                </div>
              ))}
            </div>
          </div>
        </section>
      </section>
    </main>
  );
}
