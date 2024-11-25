from fastapi import APIRouter, HTTPException 
from app.loggers.logger_setup import logger
from app.services.usuarios import registrar_usuario
from app.schemas.usuarios import UsuarioResponse, UsuarioCreate

usuarios_router = APIRouter()

@usuarios_router.post("/registrar", response_model=UsuarioResponse)
async def register_user(user_create: UsuarioCreate):
    try:
        logger.info(f"Registrando nuevo usuario con email: {user_create.email}")
        new_user = await registrar_usuario(user_create)
        logger.info(f"Usuario con email {user_create.email} registrado exitosamente.")
        return new_user
    except Exception as e:
        logger.error(f"Error al registrar al usuario con email {user_create.email}: {e}")
        raise HTTPException(status_code=500, detail="Error al registrar el usuario")
