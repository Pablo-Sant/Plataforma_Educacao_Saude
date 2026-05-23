from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Não faz sentido ter schema para pergunta, pois somos nós que iremos colocar no banco de dados, não será necessário uso de API. Mas vou apagar depois

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
    
    
    model_config = {
    "from_attributes": True
}