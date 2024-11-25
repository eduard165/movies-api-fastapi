from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings 
from app.loggers.logger_setup import logger

mongo_client = None

async def connect_to_db():
    global mongo_client
    try:
        mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
        logger.info(f"Conexión a MongoDB establecida en: {settings.MONGO_URI}")
    except Exception as e:
        logger.error(f"Error al conectar a la base de datos MongoDB: {e}")
        raise Exception(f"Error al conectar a la base de datos MongoDB: {e}")

async def close_db_connection():
    try:
        if mongo_client:
            mongo_client.close()
            logger.info("Conexión con MongoDB cerrada.")
        else:
            logger.warning("No hay conexión abierta para cerrar.")
    except Exception as e:
        logger.error(f"Error al cerrar la conexión a MongoDB: {e}")
        raise Exception(f"Error al cerrar la conexión a MongoDB: {e}")

def get_db_client():
    if mongo_client is None:
        raise Exception("No se ha establecido una conexión con MongoDB.")
    return mongo_client

def get_db():
    client = get_db_client()
    db = client[settings.DB_NAME]  
    logger.info("Accediendo a la base de datos")
    return db

def get_collection(collection_name: str):
    db = get_db()
    collection = db[collection_name] 
    logger.info(f"Accediendo a la colección '{collection_name}'")
    return collection
