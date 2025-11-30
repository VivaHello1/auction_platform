import os
from urllib.parse import quote_plus

from pydantic import ConfigDict, computed_field
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "postgres"
    POSTGRES_SCHEMA: str = "api"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:  # noqa: N802
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{quote_plus(self.POSTGRES_PASSWORD)}@{self.POSTGRES_HOST}:5432/"
            f"{self.POSTGRES_DB}"
        )


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"

    # Application settings
    PROJECT_NAME: str = "Autobid API"
    PROJECT_VERSION: str = "1.0.0"

    # Nested settings - will be populated in create_settings
    postgres: PostgresSettings

    @computed_field
    @property
    def is_test(self) -> bool:
        return self.ENVIRONMENT == "test"

    @computed_field
    @property
    def is_dev(self) -> bool:
        return self.ENVIRONMENT == "development"

    @computed_field
    @property
    def is_prod(self) -> bool:
        return self.ENVIRONMENT == "production"


def create_settings() -> Settings:
    """Factory function to create settings with appropriate env file."""
    env = os.getenv("ENVIRONMENT", "test")

    if env == "production":
        env_file = ".env.prod"
    elif env == "development":
        env_file = ".env.development"
    elif env == "test":
        env_file = ".env.test"
    else:
        env_file = ".env"

    # Create dynamic classes with the appropriate env file
    class ConfiguredPostgresSettings(PostgresSettings):
        model_config = ConfigDict(extra="ignore", env_file=env_file)

    class ConfiguredSettings(Settings):
        model_config = ConfigDict(extra="ignore", env_file=env_file)

    # Create instances of each settings class
    postgres_settings = ConfiguredPostgresSettings()

    # Create main settings with nested objects
    main_settings = ConfiguredSettings(postgres=postgres_settings)

    return main_settings


settings: Settings = create_settings()
