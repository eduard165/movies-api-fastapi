from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UsuarioBase(BaseModel):
    nombre: str = Field(..., max_length=50)
    email: EmailStr = Field(...)
    password: str= Field(..., min_length=1 , max_length=100)



class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8)


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None) 

class UsuarioResponse(UsuarioBase):
    id: str = Field(...)

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str
