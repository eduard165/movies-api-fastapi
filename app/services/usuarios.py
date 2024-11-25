from fastapi import HTTPException
from app.db.conexion import get_collection
from app.schemas.usuarios import UsuarioCreate, UsuarioResponse
from app.services.auth import hash_password
from app.loggers.logger_setup import logger

async def registrar_usuario(user_create: UsuarioCreate) -> UsuarioResponse:
    try:
        logger.info(f"Registrando usuario {user_create.email}")
        collection = get_collection("users_collection")
        
        if await collection.find_one({"email": user_create.email}):
            logger.warning(f"El email {user_create.email} ya está en uso.")
            raise HTTPException(status_code=400, detail="El email ya está en uso")
        
        hashed_password = hash_password(user_create.password)
        user_data = user_create.dict()
        user_data["password"] = hashed_password 

        result = await collection.insert_one(user_data)
        new_user = await collection.find_one({"_id": result.inserted_id})

        if not new_user:
            logger.error(f"Error al registrar el usuario.")
            raise HTTPException(status_code=500, detail="Error al registrar el usuario.")
        
        logger.info(f"Usuario {user_create.email} registrado exitosamente.")
        
        new_user["id"] = str(new_user["_id"])
        del new_user["_id"]
        return UsuarioResponse(**new_user)
    
    except Exception as e:
        logger.error(f"Error inesperado al registrar el usuario: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado al registrar el usuario.")
