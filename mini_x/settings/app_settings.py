from enum import Enum
from functools import lru_cache

from pydantic_settings import BaseSettings

from mini_x.constants import (
    LOG_LEVEL_DEFAULT,
    ENABLE_ACCESS_LOG_DEFAULT,
    ENABLE_RELOAD_DEFAULT,
    SERVER_HOST_DEFAULT,
    SERVER_PORT_DEFAULT,
)


class LogLevel(str, Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AppSettings(BaseSettings):
    server_host: str = SERVER_HOST_DEFAULT
    server_port: int = SERVER_PORT_DEFAULT
    log_level: LogLevel = LogLevel(LOG_LEVEL_DEFAULT)

    enable_access_log: bool = ENABLE_ACCESS_LOG_DEFAULT
    enable_reload: bool = ENABLE_RELOAD_DEFAULT


@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()
