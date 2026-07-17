from pytz import timezone
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from backend.models.user_model import UserModel
from backend.core.configs import settings
from backend.core.security import verificar_senha
from pydantic import EmailStr
from backend.exceptions.users_exceptions import UsuarioNaoCadastrado, EmailOuSenhaIncorretos

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
) 

async def autenticar(cpf: str, senha: str, db: AsyncSession) -> Optional[UserModel]:
    result = await db.execute( # O await só é usado quando for fazer uma operação no banco
        select(UserModel).filter(UserModel.cpf == cpf)
    )
    
    usuario = result.scalars().unique().one_or_none()
    
    if not usuario:
        raise UsuarioNaoCadastrado
    
    if not verificar_senha(senha, usuario.senha_hash):
        raise EmailOuSenhaIncorretos
    
    return usuario


def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3  Informações do payload
    payload = {}
    
    sp = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=sp) + tempo_vida # calcula quando vai expirar, que é agora + 1 semana
    
    payload['type'] = tipo_token
    
    payload['exp'] = expira
    
    payload['iat'] = datetime.now(tz=sp)
    
    payload['sub'] = str(sub)
    
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def criar_token_acesso(sub: str) -> str:
    """
    https://jwt.io
    """
    return _criar_token(
        tipo_token='acess_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )