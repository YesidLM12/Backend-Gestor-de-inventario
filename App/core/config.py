from pydantic import AnyHttpUrl
from pydantic.functional_validators import field_validator
from pydantic_settings import BaseSettings
from typing import List, Union

class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SQLALCHEMY_DATABASE_URI: str

    @field_validator("SQLALCHEMY_DATABASE_URI")
    def validate_sqlalchemy_database_uri(cls, v):
        if not v.startswith("sqlite://") and not v.startswith("postgresql://"):
            raise ValueError("Invalid SQLALCHEMY_DATABASE_URI")
        return v
    
    PORT: int = 8000

    BACKEND_CORS_ORIGINS: List[Union[str,AnyHttpUrl]] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return [i.strip() for i in v]
        raise ValueError(v) 

    class Config:
        env_file = ".env"
        case_sensitive = True
    
    settings = Settings()

    def print_settings():
        print("\n" + "="*50)
        print("⚙️  CONFIGURACIÓN DE LA APLICACIÓN")
        print("="*50)
        print(f"📦 Proyecto: {settings.PROJECT_NAME} v{settings.VERSION}")
        print(f"🐛 Debug: {settings.DEBUG}")
        print(f"🌐 API Base: {settings.API_V1_STR}")
        print(f"🗄️  Database: {settings.DATABASE_URL[:30]}...")
        print(f"🔐 Secret Key: {'✓ Configurada' if settings.SECRET_KEY else '✗ Falta'}")
        print(f"⏰ Token expira en: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} min")
        print(f"🔗 CORS Origins: {len(settings.BACKEND_CORS_ORIGINS)} configurados")
        print("="*50 + "\n")


        if __name__ == "__main__":
                print_settings()