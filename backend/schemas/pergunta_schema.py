from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PerguntaBase(BaseModel):
    texto: str
    tipo: str
    
    
class PerguntaInput(PerguntaBase):
    pass


class PerguntaUpdate(BaseModel):
    texto: Optional[str] = None
    tipo: Optional[str] = None
    
    
class PerguntaResponse(PerguntaBase):
    id: int
    created_at: datetime