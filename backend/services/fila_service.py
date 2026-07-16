from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, case

from backend.models.fila_model import FilaModel
from backend.schemas.fluxo_schema import ClassificacaoUrgencia

def gerar_prefixo(classificacao: ClassificacaoUrgencia):

    if classificacao == ClassificacaoUrgencia.ALTA:
        return "A"

    elif classificacao == ClassificacaoUrgencia.MEDIA:
        return "B"

    return "C"


async def gerar_codigo(
    db: AsyncSession,
    classificacao: ClassificacaoUrgencia
):

    prefixo = gerar_prefixo(classificacao)

    result = await db.execute(
        select(FilaModel.codigo)
        .where(
            FilaModel.codigo.like(f"{prefixo}%")
        )
    )

    codigos = result.scalars().all()

    maior = 0

    for codigo in codigos:

        try:
            numero = int(codigo[1:])

            if numero > maior:
                maior = numero

        except ValueError:
            pass

    return f"{prefixo}{maior + 1:03d}"


async def salvar_na_fila(
    db: AsyncSession,
    atendimento_id: int,
    classificacao: ClassificacaoUrgencia,
    pontuacao: int
):

    result = await db.execute(
        select(FilaModel)
        .where(
            FilaModel.atendimento_id == atendimento_id
        )
    )

    fila = result.scalars().first()

    if fila:

        fila.classificacao = classificacao
        fila.pontuacao = pontuacao

    else:

        codigo = await gerar_codigo(
            db,
            classificacao
        )

        fila = FilaModel(
            atendimento_id=atendimento_id,
            codigo=codigo,
            classificacao=classificacao,
            pontuacao=pontuacao
        )

        db.add(fila)

    await db.commit()
    await db.refresh(fila)

    return fila


async def listar_fila(
    db: AsyncSession
):

    prioridade = case(
        (FilaModel.classificacao == ClassificacaoUrgencia.ALTA, 1),
        (FilaModel.classificacao == ClassificacaoUrgencia.MEDIA, 2),
        else_=3
    )

    result = await db.execute(
        select(FilaModel)
        .order_by(
            prioridade,
            FilaModel.criado_em.asc()
        )
    )

    return result.scalars().all()


async def buscar_por_codigo(
    db: AsyncSession,
    codigo: str
):

    result = await db.execute(
        select(FilaModel)
        .where(
            FilaModel.codigo == codigo
        )
    )

    return result.scalars().first()


async def buscar_por_atendimento(
    db: AsyncSession,
    atendimento_id: int
):

    result = await db.execute(
        select(FilaModel)
        .where(
            FilaModel.atendimento_id == atendimento_id
        )
    )

    return result.scalars().first()


async def remover_da_fila(
    db: AsyncSession,
    codigo: str
):

    fila = await buscar_por_codigo(
        db,
        codigo
    )

    if fila is None:
        return None

    await db.delete(fila)
    await db.commit()

    return fila


async def chamar_proximo(
    db: AsyncSession
):

    prioridade = case(
        (FilaModel.classificacao == ClassificacaoUrgencia.ALTA, 1),
        (FilaModel.classificacao == ClassificacaoUrgencia.MEDIA, 2),
        else_=3
    )

    result = await db.execute(
        select(FilaModel)
        .order_by(
            prioridade,
            FilaModel.criado_em.asc()
        )
    )

    return result.scalars().first()