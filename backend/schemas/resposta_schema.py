from pydantic import BaseModel
from typing import Optional


class RespostaModel(BaseModel):
    resposta: str
    
    
class RespostaInput(RespostaModel):
    pass


class RespostaUpdate(BaseModel):
    resposta: Optional[str] = None
    
    
class RespostaResponse(RespostaModel):
    id: int
    atendimento_id: int
    pergunta_id: int
    opcao_pergunta_id: int
    
    model_config = {
    "from_attributes": True
}
    