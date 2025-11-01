from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SQLALCHEMY_DATABASE_URI: str
    
    PORT: int = 8000

    BACKEND_CORS_ORIGINS: List = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True
    
    settings = Settings()