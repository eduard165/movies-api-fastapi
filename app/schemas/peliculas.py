from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class PeliculaBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    actores: List[str] = Field(...)
    director: str = Field(..., max_length=100)
    genero: List[str] = Field(...)
    calificacion: float = Field(..., ge=0, le=10)
    anio_lanzamiento: int = Field(..., ge=1888)

    @field_validator("actores", "genero")
    def validate_list_not_empty(cls, value):
        if not value:
            raise ValueError("La lista no puede estar vacía.")
        return value


class PeliculaCreate(PeliculaBase):
    pass


class PeliculaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    actores: Optional[List[str]] = None
    director: Optional[str] = Field(None, max_length=100)
    genero: Optional[List[str]] = None
    calificacion: Optional[float] = Field(None, ge=0, le=10)
    anio_lanzamiento: Optional[int] = Field(None, ge=1888)


class PeliculaResponse(PeliculaBase):
    id: str = Field(...)
