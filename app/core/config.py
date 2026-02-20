from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Inventory API"
    DEBUG: bool = False
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    POSTGRES_PASSWORD:str
    SECRET_KEY:str = "CHANGE_ME"

    ACCESS_TOKEN_SECRET_KEY: str
    REFRESH_TOKEN_SECRET_KEY: str

    JWT_ISSUER: str = "inventory-api"
    JWT_AUDIENCE: str = "inventory-api-clients"
    
    ALGORITHM :str= "HS256"

    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    model_config = ConfigDict(env_file=".env")


settings = Settings()
