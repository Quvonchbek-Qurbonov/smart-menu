from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    #Mode
    DEBUG: bool = False

    # Application Settings
    APP_NAME: str = "Challenges Controller"
    APP_VERSION: str = "1.0.0"

    #Database
    DATABASE_URL: str

    #JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = "app/.env"


settings = Settings()