from fastapi import APIRouter, HTTPException, Depends
from app.schemas.peliculas import PeliculaCreate, PeliculaUpdate, PeliculaResponse
from app.models.peliculas import PeliculaInDB
from app.services.peliculas import (
    obtener_pelicula_por_nombre,
    agregar_pelicula,
    actualizar_pelicula,
    eliminar_pelicula,
    obtener_pelicula_por_id,
    obtener_todas_las_peliculas
)
from app.loggers.logger_setup import logger
from app.services.auth import get_current_user
from app.schemas.usuarios import UsuarioResponse

peliculas_router = APIRouter()


@peliculas_router.post("/registrar_pelicula", response_model=PeliculaResponse)
async def create_pelicula_route(pelicula_create: PeliculaCreate, current_user: UsuarioResponse = Depends(get_current_user)):
    try:
        logger.info(f"Usuario {current_user.email} está creando una nueva película: {pelicula_create.dict()}")
        pelicula = await agregar_pelicula(pelicula_create)
        logger.info(f"Película '{pelicula.nombre}' creada exitosamente.")
        return pelicula
    except Exception as e:
        logger.error(f"Error al crear la película: {e}")
        raise HTTPException(status_code=500, detail="Error al crear la película")


@peliculas_router.get("/obtener_todas_las_peliculas", response_model=list[PeliculaInDB])
async def get_peliculas_route(current_user: UsuarioResponse = Depends(get_current_user)):
    try:
        logger.info(f"Usuario {current_user.email} está solicitando todas las películas.")
        peliculas = await obtener_todas_las_peliculas()
        logger.info(f"Se obtuvieron {len(peliculas)} películas.")
        return peliculas
    except Exception as e:
        logger.error(f"Error al obtener todas las películas: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener las películas")


@peliculas_router.get("/obtener_pelicula_por_nombre/{nombre}", response_model=PeliculaInDB)
async def get_pelicula_by_name(nombre: str, current_user: UsuarioResponse = Depends(get_current_user)):
    try:
        logger.info(f"Usuario {current_user.email} está solicitando la película con nombre {nombre}.")
        pelicula = await obtener_pelicula_por_nombre(nombre)
        logger.info(f"Película con nombre {nombre} obtenida exitosamente.")

        return pelicula
    except Exception as e:
        logger.error(f"Error al obtener la película con nombre {nombre}: {e}")
        raise HTTPException(status_code=404, detail="Película no encontrada")


@peliculas_router.get("/obtener_pelicula_por_id/{pelicula_id}", response_model=PeliculaInDB)
async def get_pelicula_route(pelicula_id: str, current_user: UsuarioResponse = Depends(get_current_user)):
    try:
        logger.info(f"Usuario {current_user.email} está solicitando la película con ID {pelicula_id}.")
        pelicula = await obtener_pelicula_por_id(pelicula_id)
        logger.info(f"Película con ID {pelicula_id} obtenida exitosamente.")
        return pelicula
    except Exception as e:
        logger.error(f"Error al obtener la película con ID {pelicula_id}: {e}")
        raise HTTPException(status_code=404, detail="Película no encontrada")


@peliculas_router.put("/actualizar_pelicula/{pelicula_id}", response_model=PeliculaInDB)
async def update_pelicula_route(
    pelicula_id: str, 
    pelicula_update: PeliculaUpdate, 
    current_user: UsuarioResponse = Depends(get_current_user)
):
    try:
        logger.info(f"Usuario {current_user.email} está actualizando la película con ID {pelicula_id}.")
        updated_pelicula = await actualizar_pelicula(pelicula_id, pelicula_update)
        logger.info(f"Película con ID {pelicula_id} actualizada exitosamente.")
        return updated_pelicula
    except Exception as e:
        logger.error(f"Error al actualizar la película con ID {pelicula_id}: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar la película")


@peliculas_router.delete("/eliminar_pelicula/{pelicula_id}", response_model=dict)
async def delete_pelicula_route(pelicula_id: str, current_user: UsuarioResponse = Depends(get_current_user)):
    try:
        logger.info(f"Usuario {current_user.email} está eliminando la película con ID {pelicula_id}.")
        response = await eliminar_pelicula(pelicula_id)
        logger.info(f"Película con ID {pelicula_id} eliminada exitosamente.")
        return response
    except Exception as e:
        logger.error(f"Error al eliminar la película con ID {pelicula_id}: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar la película")
