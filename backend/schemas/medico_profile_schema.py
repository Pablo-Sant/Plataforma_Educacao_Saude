from pydantic import BaseModel, Field
from typing import Optional


class MedicoBase(BaseModel):
    CRM: str = Field(..., max_length=15)
    
    
class MedicoInput(MedicoBase):
    pass


class MedicoUpdate(BaseModel):
    CRM: Optional[str] = Field(None, max_length=15)
    
    
class MedicoResponse(BaseModel):
    id_medico: int
    CRM: str