from pydantic import BaseModel
from uuid import UUID

class MontadoraBase(BaseModel):
    nome: str
    pais: str
    ano_fundacao: int

class MontadoraCreate(MontadoraBase):
    pass

class Montadora(MontadoraBase):
    id: UUID

    class Config:
        orm_mode = True
