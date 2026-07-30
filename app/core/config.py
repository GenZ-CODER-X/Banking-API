from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    database_url:str
    secret_key:str
    access_token_expire_minutes:int
    algorithm:str
    secret_prefix_str:str
    secret_prefix_int:int
    secret_prefix_transaction:str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings=Settings()