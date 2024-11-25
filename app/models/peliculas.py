from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List


class Pelicula(BaseModel):
    nombre: str
    actores: List[str]
    director: str
    genero: List[str]
    calificacion: float
    anio_lanzamiento: int


class PeliculaInDB(Pelicula):
    id: str = Field(default_factory=lambda: str(ObjectId()))

    class Config:
        json_encoders = {
            ObjectId: str
        }
