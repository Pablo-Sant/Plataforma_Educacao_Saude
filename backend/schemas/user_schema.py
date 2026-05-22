from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum


class RoleEnum(str, Enum):
    PACIENTE = 'paciente'
    MEDICO = 'medico'
    


class UserBase(BaseModel):
    nome: str
    email: Optional[EmailStr] = None
    telefone: str = Field(..., min_length=5, max_length=20)
    cpf: str = Field(..., max_length=11)
    data_criacao: Optional[datetime] = None
    role: RoleEnum
    idade: Optional[int] = Field(None, ge=0, le=150)
    crm: Optional[str] = Field(None, max_length=15)
    
    
class UserInput(UserBase):
    pass


class UserUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = Field(None, min_length=5, max_length=20)
    cpf: Optional[str] = Field(None, max_length=11)
    senha: Optional[str] = None
    role: Optional[RoleEnum]
    
    
class UserResponse(UserBase):
    id: int
    data_criacao: datetime
    