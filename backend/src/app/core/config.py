# app/core/config.py

from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TESTING: bool = False

    # Application
    app_name: str = Field(default='Finance Manager', alias='APP_NAME')
    environment: str = Field(default='development', alias='ENVIRONMENT')
    debug: bool = Field(default=False, alias='DEBUG')

    # Database Credentials
    postgres_host: str = Field(alias='POSTGRES_HOST')
    postgres_port: int = Field(default=5432, alias='POSTGRES_PORT')
    postgres_user: str = Field(alias='POSTGRES_USER')
    postgres_password: str = Field(alias='POSTGRES_PASSWORD')
    postgres_db: str = Field(alias='POSTGRES_DB')

    # SQLAlchemy Pool Settings
    db_pool_size: int = Field(default=10, alias='DB_POOL_SIZE')
    db_max_overflow: int = Field(default=20, alias='DB_MAX_OVERFLOW')

    # Secret Settings
    secret_key: str = Field(alias='SECRET_KEY')
    access_token_expire_minutes: int = Field(
        default=30, alias='ACCESS_TOKEN_EXPIRE_MINUTES'
    )

    log_level: str = Field(default='INFO', alias='LOG_LEVEL')

    # Pydantic Config
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    # Computed Properties
    @property
    def database_url(self) -> str:
        return (
            f'postgresql+asyncpg://'
            f'{self.postgres_user}:{self.postgres_password}'
            f'@{self.postgres_host}:{self.postgres_port}'
            f'/{self.postgres_db}'
        )

    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        valid_levels: set[str] = {
            'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}

        upper: str = value.upper()

        if upper not in valid_levels:
            raise ValueError(
                f"Invalid LOG_LEVEL '{value}'. Must be one of {valid_levels}."
            )

        return upper


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
