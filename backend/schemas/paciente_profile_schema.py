from pydantic import BaseModel, Field
from typing import Optional


class PacienteBase(BaseModel):
    idade: int = Field(..., ge=0, le=150)
    
    
class PacienteInput(PacienteBase):
    pass


class PacienteUpdate(BaseModel):
    idade: Optional[int] = Field(None, ge=0, le=150)
    
    
class PacienteResponse(BaseModel):
    id_paciente: int