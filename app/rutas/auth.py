from fastapi import APIRouter, HTTPException, Form, Depends
from datetime import timedelta
from app.loggers.logger_setup import logger
from app.services.auth import authenticate_user, create_access_token, get_current_user
from app.schemas.usuarios import  UsuarioResponse, Token
from app.config import settings

auth_router = APIRouter()

@auth_router.post("/login", response_model=Token)
async def login_for_access_token(email: str = Form(..., description="Email del usuario"),  password: str = Form(..., description="Contraseña del usuario") ):
    
    try:
        logger.info(f"Iniciando sesión para el usuario con email: {email}")
        
        user = await authenticate_user(email, password)
        if not user:
            logger.warning(f"Usuario con email {email} no encontrado o contraseña incorrecta.")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
        
        logger.info(f"Usuario con email {email} autenticado correctamente. Token generado.")
        return {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as e:

        logger.error(f"Error al intentar iniciar sesión para el usuario con email {email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@auth_router.get("/me", response_model=UsuarioResponse)
async def read_users_me(current_user: UsuarioResponse = Depends(get_current_user)):
   
    try:
        logger.info(f"Obteniendo datos para el usuario {current_user.email}")
        return current_user
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener los datos del usuario {current_user.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener los datos del usuario")
