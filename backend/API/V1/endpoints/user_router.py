from fastapi import APIRouter, Depends, HTTPException, status
from backend.schemas.user_schema import UserInput, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session
from backend.services.user_service import UserService
from backend.exceptions.users_exceptions import UserJaExistente, PacientePrecisaIdade, MedicoPrecisaCRM


router = APIRouter()


@router.post('/cadastro', response_model=UserResponse, status_code=201)
async def post_user(payload: UserInput, db: AsyncSession = Depends(get_session)):
    
    try:
        return await UserService.cadastrar(payload, db)
    
    except UserJaExistente:
        raise HTTPException(detail = 'Usuário já cadastrado', status_code = status.HTTP_409_CONFLICT)
    
    except PacientePrecisaIdade:
        raise HTTPException(detail = 'Preenchimento da idade é obrigatório', status_code = status.HTTP_422_UNPROCESSABLE_CONTENT)
    
    except MedicoPrecisaCRM:
        raise HTTPException(detail =' Preenchimento do CRM é obrigatório', status_code = status.HTTP_422_UNPROCESSABLE_CONTENT)