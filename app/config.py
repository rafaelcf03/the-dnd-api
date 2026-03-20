from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    MONGO_URI: str = model_config.get("MONGO_URI")
    MONGO_DB_NAME: str = "dnd_api"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True


settings = Settings()
