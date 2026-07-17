from groq import AsyncGroq
from backend.core.configs import settings

client = AsyncGroq(api_key=settings.GROQ_API_KEY)


async def gerar_resumo_ia(
    classificacao_risco: str,
    classificacao_triagem: str,
    pontuacao_total: int,
    respostas: list[dict]  # ex: [{"pergunta": "...", "resposta": "..."}]
) -> str:

    respostas_formatadas = "\n".join(
        f"- {r['pergunta']}: {r['resposta']}"
        for r in respostas
    )

    prompt = f"""Você é um assistente clínico. Gere um resumo curto e objetivo
(máximo 3 frases) para a equipe médica, com base na triagem abaixo.

Classificação de risco: {classificacao_risco}
Classificação da triagem: {classificacao_triagem}
Pontuação total: {pontuacao_total}

Respostas do paciente na triagem:
{respostas_formatadas}

Resuma de forma clara e direta, destacando o que exige atenção imediata,
se houver. Não invente sintomas que não foram informados."""

    response = await client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=200
    )

    return response.choices[0].message.content