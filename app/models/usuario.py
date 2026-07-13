from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    email: str
    senha: str

class UsuarioResponse(BaseModel):
   
    model_config = {"from_attributes": True}
    id: int
    email: str


