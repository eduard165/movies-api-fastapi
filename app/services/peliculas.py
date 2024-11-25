from app.db.conexion import get_collection
from app.schemas.peliculas import PeliculaCreate, PeliculaUpdate
from app.models.peliculas import PeliculaInDB
from fastapi import HTTPException
from bson import ObjectId
from app.loggers.logger_setup import logger

async def agregar_pelicula(pelicula_create: PeliculaCreate) -> PeliculaInDB:
    try:
        logger.info(f"Creando nueva película: {pelicula_create}")
        collection = get_collection("peliculas_collection")
        
      
        pelicula_data = pelicula_create.dict()
        result = await collection.insert_one(pelicula_data)
        logger.info(f"Pelicula insertada con ID: {result.inserted_id}")
        new_pelicula = await collection.find_one({"_id": result.inserted_id})
        logger.info(f"Película creada: {new_pelicula}")
        return PeliculaInDB(id=str(new_pelicula["_id"]), **new_pelicula)
    
    except Exception as e:

        logger.error(f"Error al agregar la película: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al agregar la película")


async def obtener_todas_las_peliculas() -> list[PeliculaInDB]:
    try:

        logger.info("Obteniendo lista de todas las películas")
        collection = get_collection("peliculas_collection")
        peliculas = await collection.find().to_list(length=100)
        logger.info(f"{len(peliculas)} películas encontradas.")
        return [PeliculaInDB(id=str(pelicula["_id"]), **pelicula) for pelicula in peliculas]
    
    except Exception as e:
        logger.error(f"Error al obtener todas las películas: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener las películas")


async def obtener_pelicula_por_id(pelicula_id: str) -> PeliculaInDB:
    try:

        logger.info(f"Obteniendo película por ID: {pelicula_id}")
        collection = get_collection("peliculas_collection")
        pelicula_id = pelicula_id.strip()
        pelicula = await collection.find_one({"_id": ObjectId(pelicula_id)})
        
        if not pelicula:
            logger.warning(f"Pelicula con ID {pelicula_id} no encontrada.")
            raise HTTPException(status_code=404, detail="Pelicula no encontrada")
        
        logger.info(f"Película encontrada: {pelicula}")
        pelicula["id"] = str(pelicula["_id"])
        return pelicula
    
    except Exception as e:

        logger.error(f"Error al obtener la película con ID {pelicula_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener la película")


async def actualizar_pelicula(pelicula_id: str, pelicula_update: PeliculaUpdate) -> PeliculaInDB:
    try:
        logger.info(f"Actualizando película con ID: {pelicula_id}")
        collection = get_collection("peliculas_collection")
        update_data = pelicula_update.dict(exclude_unset=True)
        result = await collection.update_one({"_id": ObjectId(pelicula_id)}, {"$set": update_data})
        
        if result.matched_count == 0:
            logger.warning(f"Pelicula con ID {pelicula_id} no encontrada.")
            raise HTTPException(status_code=404, detail="Pelicula no encontrada")
        
        logger.info(f"Película con ID {pelicula_id} actualizada.")
        updated_pelicula = await collection.find_one({"_id": ObjectId(pelicula_id)})

        if not updated_pelicula:
            logger.warning(f"Pelicula con ID {updated_pelicula} no encontrada.")
            raise HTTPException(status_code=404, detail="Pelicula no encontrada")
        
        logger.info(f"Pelicula con ID {updated_pelicula} actualizada exitosamente.")
        return PeliculaInDB(id=str(updated_pelicula["_id"]), **updated_pelicula)
    
    except Exception as e:

        logger.error(f"Error al actualizar la película con ID {pelicula_id}: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar la película")


async def eliminar_pelicula(pelicula_id: str) -> dict:
    try:

        logger.info(f"Eliminando película con ID: {pelicula_id}")
        collection = get_collection("peliculas_collection")
        result = await collection.delete_one({"_id": ObjectId(pelicula_id)})
        
        if result.deleted_count == 0:
            logger.warning(f"Pelicula con ID {pelicula_id} no encontrada.")
            raise HTTPException(status_code=404, detail="Pelicula no encontrada")
        
        logger.info(f"Pelicula con ID {pelicula_id} eliminada exitosamente.")
        return {"message": "Pelicula eliminada exitosamente"}
    
    except Exception as e:

        logger.error(f"Error al eliminar la película con ID {pelicula_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al eliminar la película")


async def obtener_pelicula_por_nombre(name: str) -> PeliculaInDB:
    try:

        logger.info(f"Obteniendo película por nombre {name}")
        collection = get_collection("peliculas_collection")
        pelicula = await collection.find_one({"nombre": {"$regex": f"^{name}$", "$options": "i"}})
        
        if pelicula:
            logger.info(f"Película encontrada: {pelicula}")
            return PeliculaInDB(id=str(pelicula["_id"]), **pelicula)
        else:
            logger.warning(f"Pelicula con nombre {name} no encontrada.")
            return None
        
    except Exception as e:

        logger.error(f"Error al obtener la película con nombre {name}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener la película")
