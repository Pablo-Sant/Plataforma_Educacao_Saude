from pydantic import BaseModel


class AlertaModel(BaseModel):
    texto: str


class AlertaInput(AlertaModel):
    pass


class AlertaResponse(AlertaModel):
    id: int
    atendimento_id: int
    
    
    model_config = {
    "from_attributes": True
}