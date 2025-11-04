from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "change_me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    DATABASE_URL: str = "sqlite:///./scoutverein.db"
    EMAIL_SENDER: str = "notifications@scoutverein.local"
    EMAIL_ADMIN: str = "admin@verein.de"
    ADMIN_EMAIL: str = "admin@verein.de"
    ADMIN_PASSWORD: str = "admin123"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()