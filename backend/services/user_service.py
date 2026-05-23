from backend.schemas.user_schema import UserInput, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.user_model import UserModel
from backend.models.paciente_profile import PacienteProfile
from backend.models.medico_profile import MedicoProfile
from backend.core.security import gerar_hash_senha
from sqlalchemy.future import select
from backend.exceptions.users_exceptions import UserJaExistente, PacientePrecisaIdade, MedicoPrecisaCRM, UsuarioInexistente
from backend.schemas.user_schema import RoleEnum
from fastapi.security import OAuth2PasswordRequestForm
from core.auth import autenticar, criar_token_acesso
from sqlalchemy.exc import SQLAlchemyError


class UserService:
    
    @staticmethod
    async def verificar_existencia(cpf: str, db: AsyncSession):
        
        result = await db.execute(
            select(UserModel).filter(UserModel.cpf == cpf)
        )
        
        user = result.scalar_one_or_none()
        
        return user
    
    
    @staticmethod
    async def cadastrar(dto: UserInput, db: AsyncSession):
        
        role = dto.role
        
        if role == RoleEnum.PACIENTE:
            if dto.idade is None:
                raise PacientePrecisaIdade
            
            
        elif role == RoleEnum.MEDICO:
            if not dto.crm:
                raise MedicoPrecisaCRM
                     
        
        user = await UserService.verificar_existencia(dto.cpf, db)
        
        if user:
            raise UserJaExistente
        
        data = dto.model_dump()
        data.pop('crm', None)
        data.pop('idade', None)
        senha_pura = data.pop('senha')
        
        user = UserModel(**data, senha_hash = gerar_hash_senha(senha_pura))
        
        
        try:
            db.add(user)
            await db.flush()
            
            if role == RoleEnum.PACIENTE:
                paciente = PacienteProfile(id= user.id, idade= dto.idade)
                db.add(paciente)
                
            elif role == RoleEnum.MEDICO:
                medico = MedicoProfile(id= user.id, crm= dto.crm)
                db.add(medico)    
            
                
            await db.commit()
            await db.refresh(user)
            
            return user
        
        except SQLAlchemyError:
            await db.rollback()
            raise 
        
        
        
    @staticmethod
    async def login(form_data: OAuth2PasswordRequestForm, db: AsyncSession) -> dict:
        
        user = await autenticar(form_data.username, form_data.password, db)
        
        return{
            'access_token': criar_token_acesso(sub=user.id),
            'token_type': 'bearer'
        }
        
        
    
    @staticmethod
    async def atualizar(dto: UserUpdate, usuario_logado: UserModel, db: AsyncSession):
        
        
        data = dto.model_dump(exclude_unset=True)
        
        if 'senha' in data:
            senha_pura = data.pop('senha')
            data['senha_hash'] = gerar_hash_senha(senha_pura)
            
        for campo, valor in data.items():
            setattr(usuario_logado, campo, valor)
            
        try:
            await db.commit()
            await db.refresh(usuario_logado)
            return usuario_logado
            
        except SQLAlchemyError:
            await db.rollback()
            raise 
        
        
    @staticmethod
    async def deletar(usuario_logado: UserModel, db: AsyncSession):
        
        try:
            await db.delete(usuario_logado)
            await db.commit()
            
        except SQLAlchemyError:
            await db.rollback()
            raise 