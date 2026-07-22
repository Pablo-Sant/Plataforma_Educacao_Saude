from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.deps import get_session
from backend.services.fila_service import listar_fila
from backend.schemas.fila_schema import FilaItemOut

router = APIRouter()


@router.get("/fila", response_model=list[FilaItemOut])
async def ver_fila(db: AsyncSession = Depends(get_session)):
    atendimentos = await listar_fila(db)

    return [
        FilaItemOut(
            id=a.id,
            paciente_id=a.paciente_id,
            paciente_nome=(
                a.paciente.user.nome
                if a.paciente and a.paciente.user
                else f"Paciente #{a.paciente_id}"
            ),
            classificacao_risco=a.classificacao_risco,
            classificacao_triagem=a.classificacao_triagem,
            data_atendimento=a.data_atendimento,
        )
        for a in atendimentos
    ]