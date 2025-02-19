"""Config data."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class PGConfig(BaseSettings):
    """Database config."""

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_DB_NAME: str = "mydb"
    PG_USER: str = "user"
    PG_PASSWORD: str = "password"

    @property
    def url_async(self):
        """Config a link to database connection for asyncpg."""
        # postgresql+asyncpg://postgres:postgres@localhost:5432/db_name
        return (
            "postgresql+asyncpg://"
            f"{self.PG_USER}:{self.PG_PASSWORD}@"
            f"{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB_NAME}"
        )

    @property
    def local_url_async(self):
        """Use this method for local connections."""
        # postgresql+asyncpg://postgres:postgres@localhost:5432/db_name
        container_ip: str = "192.168.1.2"
        return (
            "postgresql+asyncpg://"
            f"{self.PG_USER}:{self.PG_PASSWORD}@"
            f"{container_ip}:{self.PG_PORT}/{self.PG_DB_NAME}"
        )


pg_config = PGConfig()
