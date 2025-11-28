from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Smart Menu"
    APP_VERSION: str = "1.0.0"

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    SENDER_EMAIL: str
    APP_PASSWORD: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }


settings = Settings()
