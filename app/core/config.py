from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Inventory API"
    DEBUG: bool = True
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    POSTGRES_PASSWORD:str
    SECRET_KEY:str = "CHANGE_ME"
    ALGORITHM :str= "HS256"

    model_config = ConfigDict(env_file=".env")


settings = Settings()
