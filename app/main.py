from fastapi import FastAPI
from app.loggers.logger_setup import logger
from app.rutas.peliculas import peliculas_router
from app.rutas.usuarios import  usuarios_router
from app.db.conexion import connect_to_db, close_db_connection
from app.rutas.auth import auth_router

app = FastAPI(
    title="Películas API",
    description="API RESTful para gestión de películas con autenticación JWT",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_db_client():
    logger.info("Iniciando la conexión con MongoDB")
    await connect_to_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Cerrando la conexión con MongoDB")
    await close_db_connection()

@app.get("/")
async def root():
    logger.info("Accediendo a la ruta raíz")
    return {"message": "Bienvenido a la API de películas"}

app.include_router(peliculas_router, prefix="/peliculas", tags=["Películas"])
app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
app.include_router(usuarios_router, prefix="/usuarios", tags=["Usuarios"])
