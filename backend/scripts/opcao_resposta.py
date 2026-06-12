import asyncio
from backend.core.database import SessionLocal
from backend.models.__all_models import *


opcao_resposta = [

    # 1. Falta de ar intensa?
    {
        'texto': 'sim',
        'pergunta_id': 1,
        'pontuacao_risco': 10,
        'classificacao': 'EMERGENCIA_RESPIRATORIA',
        'encerra_fluxo': True
    },
    {
        'texto': 'não',
        'pergunta_id': 1,
        'proxima_pergunta_id': 2,
        'pontuacao_risco': 0
    },

    # 2. Dor no peito?
    {
        'texto': 'sim',
        'pergunta_id': 2,
        'pontuacao_risco': 10,
        'classificacao': 'EMERGENCIA_CARDIACA',
        'encerra_fluxo': True
    },
    {
        'texto': 'não',
        'pergunta_id': 2,
        'proxima_pergunta_id': 4,
        'pontuacao_risco': 0
    },

    # 4. Sangramento?
    {
        'texto': 'sim',
        'pergunta_id': 4,
        'pontuacao_risco': 10,
        'classificacao': 'HEMORRAGIA_POSSIVEL',
        'encerra_fluxo': True
    },
    {
        'texto': 'não',
        'pergunta_id': 4,
        'proxima_pergunta_id': 9,
        'pontuacao_risco': 0
    },

    # 9. Está consciente?
    {
        'texto': 'sim',
        'pergunta_id': 9,
        'proxima_pergunta_id': 5,
        'pontuacao_risco': 0
    },
    {
        'texto': 'não',
        'pergunta_id': 9,
        'pontuacao_risco': 10,
        'classificacao': 'INCONSCIENCIA',
        'encerra_fluxo': True
    },

    # 5. Consegue andar normalmente?
    {
        'texto': 'sim',
        'pergunta_id': 5,
        'proxima_pergunta_id': 6,
        'pontuacao_risco': 0
    },
    {
        'texto': 'não',
        'pergunta_id': 5,
        'pontuacao_risco': 8,
        'classificacao': 'LIMITACAO_MOTORA_GRAVE',
        'encerra_fluxo': True
    },

    # 6. Tontura ou desmaios?
    {
        'texto': 'sim',
        'pergunta_id': 6,
        'proxima_pergunta_id': 21,
        'pontuacao_risco': 5
    },
    {
        'texto': 'não',
        'pergunta_id': 6,
        'proxima_pergunta_id': 3,
        'pontuacao_risco': 0
    },

    # 21. Dificuldade para enxergar?
    {
        'texto': 'sim',
        'pergunta_id': 21,
        'pontuacao_risco': 10,
        'classificacao': 'SUSPEITA_AVC',
        'encerra_fluxo': True
    },
    {
        'texto': 'não',
        'pergunta_id': 21,
        'proxima_pergunta_id': 22,
        'pontuacao_risco': 0
    },

    # 22. Dormência?
    {
        'texto': 'sim',
        'pergunta_id': 22,
        'pontuacao_risco': 10,
        'classificacao': 'SUSPEITA_AVC',
        'encerra_fluxo': True
    },
    {
        'texto': 'não',
        'pergunta_id': 22,
        'proxima_pergunta_id': 23,
        'pontuacao_risco': 0
    },

    # 23. Dificuldade para falar?
    {
        'texto': 'sim',
        'pergunta_id': 23,
        'pontuacao_risco': 10,
        'classificacao': 'SUSPEITA_AVC',
        'encerra_fluxo': True
    },
    {
        'texto': 'não',
        'pergunta_id': 23,
        'proxima_pergunta_id': 3,
        'pontuacao_risco': 0
    },

    # 3. Febre?
    {
        'texto': 'sim',
        'pergunta_id': 3,
        'proxima_pergunta_id': 17,
        'pontuacao_risco': 3
    },
    {
        'texto': 'não',
        'pergunta_id': 3,
        'proxima_pergunta_id': 10,
        'pontuacao_risco': 0
    },

    # 17. Tosse?
    {
        'texto': 'sim',
        'pergunta_id': 17,
        'pontuacao_risco': 2,
        'classificacao': 'SINDROME_RESPIRATORIA',
        'encerra_fluxo': True
    },
    {
        'texto': 'não',
        'pergunta_id': 17,
        'proxima_pergunta_id': 16,
        'pontuacao_risco': 0
    },

    # 16. Dores no corpo?
    {
        'texto': 'sim',
        'pergunta_id': 16,
        'pontuacao_risco': 1,
        'classificacao': 'SINDROME_VIRAL',
        'encerra_fluxo': True
    },
    {
        'texto': 'não',
        'pergunta_id': 16,
        'proxima_pergunta_id': 10,
        'pontuacao_risco': 0
    },

    # 10. Náusea ou vontade de vomitar?
    {
        'texto': 'sim',
        'pergunta_id': 10,
        'proxima_pergunta_id': 15,
        'pontuacao_risco': 2
    },
    {
        'texto': 'não',
        'pergunta_id': 10,
        'proxima_pergunta_id': 27,
        'pontuacao_risco': 0
    },

    # 15. Consegue beber água normalmente?
    {
        'texto': 'sim',
        'pergunta_id': 15,
        'proxima_pergunta_id': 27,
        'pontuacao_risco': 0
    },
    {
        'texto': 'não',
        'pergunta_id': 15,
        'pontuacao_risco': 5,
        'classificacao': 'RISCO_DESIDRATACAO',
        'encerra_fluxo': True
    },

    # 27. Dor abdominal?
    {
        'texto': 'sim',
        'pergunta_id': 27,
        'pontuacao_risco': 4,
        'classificacao': 'AVALIACAO_ABDOMINAL',
        'encerra_fluxo': True
    },
    {
        'texto': 'não',
        'pergunta_id': 27,
        'proxima_pergunta_id': 28,
        'pontuacao_risco': 0
    },

    # 28. Dificuldade para urinar?
    {
        'texto': 'sim',
        'pergunta_id': 28,
        'pontuacao_risco': 4,
        'classificacao': 'AVALIACAO_URINARIA',
        'encerra_fluxo': True
    },
    {
        'texto': 'não',
        'pergunta_id': 28,
        'proxima_pergunta_id': 18,
        'pontuacao_risco': 0
    },

    # 18. Alteração da pressão arterial?
    {
        'texto': 'sim',
        'pergunta_id': 18,
        'proxima_pergunta_id': 19,
        'pontuacao_risco': 5
    },
    {
        'texto': 'não',
        'pergunta_id': 18,
        'proxima_pergunta_id': 19,
        'pontuacao_risco': 0
    },

    # 19. Palpitações?
    {
        'texto': 'sim',
        'pergunta_id': 19,
        'pontuacao_risco': 5,
        'classificacao': 'ALTERACAO_CARDIOVASCULAR',
        'encerra_fluxo': True
    },
    {
        'texto': 'não',
        'pergunta_id': 19,
        'proxima_pergunta_id': 8,
        'pontuacao_risco': 0
    },

    # 8. Possui doença crônica?
    {
        'texto': 'sim',
        'pergunta_id': 8,
        'pontuacao_risco': 2,
        'classificacao': 'ACOMPANHAMENTO_CLINICO',
        'encerra_fluxo': True
    },
    {
        'texto': 'não',
        'pergunta_id': 8,
        'pontuacao_risco': 0,
        'classificacao': 'BAIXO_RISCO',
        'encerra_fluxo': True
    }

]


async def seed():
    async with SessionLocal() as db:
        for dados in opcao_resposta:
            opcao = OpcaoRespostaModel(**dados)
            db.add(opcao)
        await db.commit()
        print(f"{len(opcao_resposta)} opções respostas inseridas com sucesso.")


if __name__ == "__main__":
    async_run_func = getattr(asyncio, "run")
    async_run_func(seed())