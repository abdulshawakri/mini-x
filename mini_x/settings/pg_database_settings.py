from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from mini_x.constants import (
    PG_ENV_PREFIX,
    PG_DATABASE_DEFAULT,
    PG_PORT_DEFAULT,
    PG_HOST_DEFAULT,
    PG_PASSWORD_DEFAULT,
    PG_USERNAME_DEFAULT,
)


class PGDatabaseSettings(BaseSettings):
    username: str = PG_USERNAME_DEFAULT
    password: SecretStr = SecretStr(PG_PASSWORD_DEFAULT)
    host: str = PG_HOST_DEFAULT
    port: int = PG_PORT_DEFAULT
    database_name: str = PG_DATABASE_DEFAULT

    model_config = SettingsConfigDict(env_prefix=PG_ENV_PREFIX)


@lru_cache
def get_pg_database_settings() -> PGDatabaseSettings:
    return PGDatabaseSettings()
