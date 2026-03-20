from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    MONGO_URI: str = "mongodb+srv://rafaelcastrofreitas27_db_user:s0sB6H1QTVWyEAOy@dnd-api.0fi3ltt.mongodb.net/?appName=DND-API"
    MONGO_DB_NAME: str = "dnd_api"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True


settings = Settings()
