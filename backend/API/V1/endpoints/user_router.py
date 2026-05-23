from fastapi import APIRouter, Depends, HTTPException, status
from backend.schemas.user_schema import UserInput, UserResponse, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session, get_current_user
from backend.services.user_service import UserService
from backend.exceptions.users_exceptions import UserJaExistente,PacientePrecisaIdade, MedicoPrecisaCRM, UsuarioNaoCadastrado, EmailOuSenhaIncorretos
from schemas.token import TokenResponse
from fastapi.security import OAuth2PasswordRequestForm
from backend.models.user_model import UserModel


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
    
    
@router.post('/login', response_model=TokenResponse, status_code=200)
async def post_login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    
    try: 
        return await UserService.login(form_data, db)
    
    except UsuarioNaoCadastrado:
        raise HTTPException(detail='Usuário não cadastrado', status_code=404)
    
    except EmailOuSenhaIncorretos:
        raise HTTPException(detail='Email ou senha incorretos', status_code=401)
    

@router.get('/me', response_model=UserResponse, status_code=200)
async def get_me(usuario_logado: UserModel = Depends(get_current_user)):
    
    return usuario_logado


@router.put('/me', response_model=UserResponse, status_code=201)
async def put_user(payload: UserUpdate, usuario_logado: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    
        return await UserService.atualizar(payload, usuario_logado, db)
    


@router.delete('/me', status_code=204)
async def del_user(usuario_logado: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    
    return await UserService.deletar(usuario_logado, db)
    