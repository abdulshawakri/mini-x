from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from mini_x.constants import (
    SECRET_ACCESS_TOKEN_EXPIRE_MINUTES_DEFAULT,
    SECRET_ALGORITHM_DEFAULT,
    SECRET_ENV_PREFIX,
)


class SecretSettings(BaseSettings):
    key: str
    algorithm: str = SECRET_ALGORITHM_DEFAULT
    access_token_expire_minutes: int = SECRET_ACCESS_TOKEN_EXPIRE_MINUTES_DEFAULT

    model_config = SettingsConfigDict(env_prefix=SECRET_ENV_PREFIX)


@lru_cache
def get_secret_settings() -> SecretSettings:
    return SecretSettings()  # type: ignore[call-arg]
