from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.db.conexion import get_collection
from app.schemas.usuarios import  UsuarioResponse
from app.models.usuarios import UsuarioInDB
from app.config import settings
from fastapi import HTTPException
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from app.loggers.logger_setup import logger
from jose.exceptions import ExpiredSignatureError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  


def hash_password(password: str) -> str:
    logger.debug(f"Hashing password.")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    logger.debug(f"Verifying password.")
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Union[timedelta, int] = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)):
    logger.debug(f"Creando token de acceso para {data}")
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    logger.info(f"Token de acceso creado exitosamente para {data['sub']}.")
    return encoded_jwt

async def authenticate_user(email: str, password: str) -> UsuarioInDB:
    try:
        logger.info(f"Autenticando usuario {email}.")
        user = await get_user_by_email(email)

        if not user or not verify_password(password, user.password):
            logger.warning(f"Credenciales incorrectas para el usuario {email}.")
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")

        logger.info(f"Usuario {email} autenticado exitosamente.")
        return user

    except HTTPException as e:
        logger.warning(f"Error en la autenticación para {email}: {str(e.detail)}")
        raise e

    except Exception as e:
        logger.error(f"Error al autenticar al usuario {email}: {e}")
        raise HTTPException(status_code=500, detail="Error al autenticar el usuario.") 

async def get_user_by_email(email: str) -> UsuarioInDB:
    try:
        logger.debug(f"Obteniendo usuario por email: {email}")
        collection = get_collection("users_collection")
        user = await collection.find_one({"email": email})

        if user:
            logger.info(f"Usuario {email} encontrado.")
         
            return UsuarioInDB(**user)

        logger.warning(f"Usuario {email} no encontrado.")
        return None

    except Exception as e:
        logger.error(f"Error al obtener el usuario {email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener el usuario.")
async def get_current_user(token: str = Depends(oauth2_scheme)) -> UsuarioInDB:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        logger.info(f"Email: {email}")

        if not email:
            raise HTTPException(status_code=401, detail="No se pudo validar el token")
        
        user = await get_user_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        logger.info(f"Usuario encontrado: {user}")
        
        return user  

    except ExpiredSignatureError:
        logger.error("Token JWT ha expirado.")
        raise HTTPException(status_code=401, detail="El token ha expirado")
    except JWTError:
        logger.error("Token JWT inválido.")
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        logger.error(f"Error al obtener el usuario actual: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener el usuario actual")
