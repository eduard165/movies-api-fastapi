from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId


class Usuario(BaseModel):
    nombre: str
    email: EmailStr
    password: str


class UsuarioInDB(Usuario):
    id: str = Field(default_factory=lambda: str(ObjectId()))

    class Config:
        json_encoders = {
            ObjectId: str
        }
