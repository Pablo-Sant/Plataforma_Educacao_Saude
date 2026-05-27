from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum


class ClinicaBase(BaseModel):
    nome: str = Field(min_length= 5, max_length = 50)
    endereco: str = Field( min_length= 10, max_length = 150)
    telefone: str = Field(min_length= 11 , max_length = 15)
    email: EmailStr = Field(min_length= 15 , max_length = 50)
    senha: str = Field(min_length= 8 , max_length = 100)
    


class ClinicaInput(ClinicaBase):
    pass



class ClinicaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length= 5, max_length = 50)
    endereco: Optional[str] = Field(None, min_length= 10, max_length = 150)
    telefone: Optional[str] = Field(None, min_length= 11 , max_length = 15)
    email: Optional[EmailStr] = Field(None, min_length= 15 , max_length = 50)
    senha: Optional[str] = Field(None, min_length= 8 , max_length = 100)
    
    

class ClinicaResponse(BaseModel):
    id: int
    nome: str
    endereco: str
    telefone: str
    email: EmailStr
        

    model_confing = {
        
        'from_attributes': True
        
        }


