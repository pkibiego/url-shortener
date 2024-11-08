# config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    access_token_expires_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
