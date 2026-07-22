# 🩺 TriagemIA - Sistema Inteligente de Pré-Consulta e Apoio à Decisão Clínica

O **TriagemIA** é uma plataforma de pré-consulta que centraliza a triagem de pacientes antes do atendimento médico, combinando um fluxo de perguntas dinâmico, classificação automática de risco e geração de resumo clínico via IA. O projeto foca em uma API assíncrona de alta performance, capaz de sustentar o ciclo completo triagem → priorização → atendimento.

> ⚠️ **Projeto de estudo/portfólio.** Não é utilizado em ambiente clínico real e não substitui avaliação médica profissional. Evolução para produção exigiria validação clínica formal e adequação regulatória (LGPD, possivelmente CFM/ANVISA).

## 💼 Arquitetura de Negócio

O sistema atua como camada de apoio à decisão entre o paciente e a equipe médica, cobrindo o ciclo completo do atendimento:

- **Triagem Dinâmica**: perguntas condicionais, onde a resposta escolhida define a próxima pergunta do fluxo.
- **Classificação de Risco**: pontuação acumulada por resposta + classificações específicas para sinais críticos (emergência respiratória, cardíaca, hemorragia, inconsciência, entre outras).
- **Resumo Clínico via IA**: geração automática de resumo do caso a partir do contexto da triagem, usando LLM (Groq).
- **Fila de Atendimento Priorizada**: pacientes ordenados por gravidade clínica (alto → médio → baixo), não por ordem de chegada.
- **Gestão de Atendimentos**: ciclo de vida completo (aguardando triagem → aguardando atendimento → em atendimento → finalizado).

## 🏗️ Decisões de Engenharia

A construção do backend prioriza a separação entre orquestração HTTP, regra de negócio e persistência:

```
backend/
 ├── API/V1/endpoints/  # Rotas HTTP e orquestração de endpoints
 ├── services/          # Regras de negócio e lógica de domínio
 ├── models/             # Entidades ORM e persistência de dados
 ├── schemas/            # Contratos de entrada/saída (Pydantic)
 └── core/               # Configurações e dependências
```

- **Modularização**: cada domínio (atendimento, fluxo de triagem, fila, usuários) isolado em seu próprio service e schema.
- **Lógica de Domínio**: cálculo de risco, classificação e priorização isolados na camada de `services`, mantendo as rotas focadas em orquestração.
- **Integridade de Dados**: schemas Pydantic para validação de contratos e models SQLAlchemy para persistência relacional, incluindo enums nativos do PostgreSQL para status e classificação de risco.
- **Processamento Assíncrono**: uso de `AsyncSession` para todas as operações de banco, incluindo a chamada externa à API de IA.
- **Integração com LLM**: geração de resumo clínico contextualizado (não um chatbot genérico) via API da Groq, com fallback definido para indisponibilidade do serviço.

## 🔐 Fluxo de Triagem e Priorização

### Ciclo de vida do atendimento

1. **Criação**: atendimento criado com status `aguardando_triagem`.
2. **Triagem**: paciente responde ao fluxo dinâmico de perguntas; cada resposta contribui para a pontuação de risco.
3. **Finalização da triagem**: sistema calcula a classificação (por pontuação ou por sinal específico crítico), atualiza o atendimento para `aguardando_atendimento`, e gera o resumo via IA.
4. **Fila**: atendimento aparece na fila, ordenado por prioridade clínica real (risco alto primeiro, empate por ordem de chegada).
5. **Atendimento médico**: consulta ao atendimento individual, com resumo e classificação já disponíveis.

### Ciclo de vida do recurso (Request-Response)

```
Request → Schema Pydantic → Router → Service → Model (SQLAlchemy) → Response Schema
```

## 🛠️ Tecnologias

**Backend**
| Camada | Tecnologia |
|---|---|
| Linguagem | Python |
| Framework | FastAPI |
| Banco de Dados | PostgreSQL |
| ORM | SQLAlchemy (Async) |
| IA Generativa | Groq API (`openai/gpt-oss-20b`) |

**Frontend**
| Camada | Tecnologia |
|---|---|
| Framework | React + Vite |
| Consumo de API | Fetch com autenticação por token |

## ⚡ Quick Start (Como executar)

### Pré-requisitos
- Python 3.10+
- Conta no [Supabase](https://supabase.com) (camada gratuita já é suficiente)
- Node.js (para o frontend)
- Chave de API da Groq ([console.groq.com](https://console.groq.com))

### Backend

```bash
git clone https://github.com/seu-usuario/triagem-ia.git
cd triagem-ia/backend

python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

Copie o arquivo de exemplo e preencha com suas próprias credenciais:
```bash
cp .env.example .env
```

```
DATABASE_URL=postgresql+asyncpg://postgres:[SUA_SENHA]@[SEU_HOST].supabase.co:5432/postgres
GROQ_API_KEY=sua_chave_aqui
```

> Cada pessoa que rodar o projeto precisa criar seu próprio projeto no Supabase (gratuito) e gerar sua própria `DATABASE_URL` — as credenciais acima são só um exemplo de formato, não devem ser reais nem compartilhadas.

**Como pegar sua `DATABASE_URL` no Supabase:**
1. Crie um projeto em [supabase.com](https://supabase.com) (gratuito).
2. No painel do projeto, vá em **Project Settings → Database**.
3. Em **Connection string**, selecione o modo **URI** e o driver **asyncpg** (ou copie a versão padrão e troque `postgresql://` por `postgresql+asyncpg://`, que é o formato exigido pelo SQLAlchemy async).
4. Substitua `[YOUR-PASSWORD]` pela senha do banco definida na criação do projeto.

> ⚠️ Certifique-se de que `.env` está no `.gitignore` do projeto — nunca commite credenciais reais, nem no histórico do Git.

Crie as tabelas e inicie a API:
```bash
uvicorn main:app --reload
```

📍 Documentação interativa em: `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd triagem-ia/frontend
npm install
npm run dev
```

## 📊 Status do Projeto e Maturidade

| Recurso | Status | Observação |
|---|---|---|
| Arquitetura Base | ✅ Concluído | Estrutura modular (Services/Models/Schemas). |
| Fluxo de Triagem Dinâmico | ✅ Implementado | Perguntas condicionais com encadeamento. |
| Classificação de Risco | ✅ Implementado | Pontuação + classificação específica por resposta crítica. |
| Resumo Clínico via IA | ✅ Implementado | Integração com Groq, com fallback em caso de falha. |
| Fila Priorizada | ✅ Implementado | Ordenação por risco + tempo de espera. |
| Autenticação | 🔐 Parcial | Login por papel (paciente/médico) implementado; autorização granular por rota em evolução. |
| Alertas Clínicos Estruturados | 🏗️ Em progresso | Hoje embutido no texto do resumo; planejado separar em campo próprio. |
| Testes Automatizados | ⏳ Planejado | Próxima fase do roadmap. |
| Logging e Observabilidade | ⏳ Planejado | Próxima fase do roadmap. |
| Deploy/CI-CD | ⏳ Planejado | Tentativa de deploy na AWS em andamento. |

## 🐛 Limitações Conhecidas

- Reabrir/reacessar o mesmo atendimento pode acumular pontuação de risco indevidamente (correção planejada).
- O enum de classificação específica de triagem se mostrou genérico demais para o domínio clínico e está sendo redesenhado para algo mais granular.
- Autorização por papel hoje é reforçada principalmente no frontend; validação de escopo no backend está em evolução.

## 🚀 Próximos Passos (Evolução do Sistema)

- Aprofundar um domínio clínico específico (ex: triagem cardiovascular) antes de expandir para outros.
- Testes automatizados (pytest + pytest-asyncio) cobrindo os fluxos críticos.
- Logging estruturado, especialmente em torno da chamada externa à API de IA.
- Separar alertas clínicos do texto do resumo, com estrutura própria.
- Deploy em produção (AWS).

## 🏆 Diferencial

Não é um formulário que apenas salva dados. O sistema **interpreta respostas**, **toma decisão** (classificação de risco) e **organiza o atendimento** de acordo com essa decisão — com uma camada de IA generativa aplicada a um caso de uso real de apoio à decisão clínica.

## 👤 Autor

Pablo Sant
Engenharia de Software | Backend Python | Integração com IA
