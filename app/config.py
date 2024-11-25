import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI MongoDB Users")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "1.0.0")
    MONGO_URI: str = os.getenv("MONGO_URI") 
    DB_NAME: str = os.getenv("DB_NAME")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()
