import asyncio
from backend.core.database import SessionLocal
from backend.models.__all_models import *


## tipo de perguntas ainda discutível
##tipo de perguntas discutivel

'''
perguntas = [
    {
        "texto": "Você está sentindo falta de ar?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Está com dor no peito?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Você teve febre nas últimas 24 horas?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Está apresentando sangramento?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Você consegue andar normalmente?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Está sentindo tontura ou desmaios?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Está sentindo dor intensa?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Você possui alguma doença crônica?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Está consciente e respondendo normalmente?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Os sintomas começaram hoje?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Você está sentindo náusea?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Você vomitou nas últimas 24 horas?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Está sentindo dor de cabeça?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Você está conseguindo se alimentar normalmente?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Está conseguindo beber água normalmente?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Você sente dores no corpo?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Está com tosse?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Você percebeu alteração na pressão arterial?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Está sentindo palpitações ou coração acelerado?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Você teve alguma queda ou acidente recentemente?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Está com dificuldade para enxergar?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Você sente dormência em alguma parte do corpo?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Está com dificuldade para falar?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Você tem alergia a algum medicamento?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Fez uso de algum medicamento nas últimas 24 horas?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Você possui histórico de cirurgias?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Está sentindo dores abdominais?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Está com dificuldade para urinar?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Você está dormindo normalmente?",
        "tipo": "sim_nao"
    },
    {
        "texto": "Já precisou de internação recentemente?",
        "tipo": "sim_nao"
    }
]


'''

perguntas = [
    {
        "texto": "Você está sentindo falta de ar intensa ou dificuldade para respirar?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Está com dor no peito?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Você teve febre nas últimas 24 horas?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Está apresentando sangramento?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Você consegue andar normalmente?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Está sentindo tontura ou desmaios?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Qual o nível da sua dor atualmente?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Você possui alguma doença crônica?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Está consciente e respondendo normalmente?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Os sintomas começaram quando?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Você está sentindo náusea ou vontade de vomitar?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Você vomitou nas últimas 24 horas?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Está sentindo dor de cabeça?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Você está conseguindo se alimentar normalmente?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Está conseguindo beber água normalmente?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Você sente dores no corpo?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Está com tosse?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Você percebeu alteração na pressão arterial recentemente?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Está sentindo palpitações ou coração acelerado?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Você teve alguma queda ou acidente recentemente?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Está com dificuldade para enxergar?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Você sente dormência em alguma parte do corpo?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Está com dificuldade para falar?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Você tem alergia a algum medicamento?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Fez uso de algum medicamento nas últimas 24 horas?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Você possui histórico de cirurgias?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Está sentindo dores abdominais?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Está com dificuldade para urinar?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Você está dormindo normalmente?",
        "tipo": "multipla_escolha"
    },
    {
        "texto": "Já precisou de internação recentemente?",
        "tipo": "multipla_escolha"
    }
]

async def seed():
    async with SessionLocal() as db:
        for dados in perguntas:
            pergunta = PerguntaModel(**dados)
            db.add(pergunta)
        await db.commit()
        print(f"{len(perguntas)} pergunta inserida com sucesso.")


if __name__ == "__main__":
    asyncio.run(seed())