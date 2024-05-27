from enum import Enum
from functools import lru_cache

from pydantic_settings import BaseSettings

from mini_x.constants import (
    LOG_LEVEL_DEFAULT,
    ENABLE_ACCESS_LOG,
    ENABLE_RELOAD,
    SERVER_HOST,
    SERVER_PORT,
)


class LogLevel(str, Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AppSettings(BaseSettings):
    server_host: str = SERVER_HOST
    server_port: int = SERVER_PORT
    log_level: LogLevel = LogLevel(LOG_LEVEL_DEFAULT)

    enable_access_log: bool = ENABLE_ACCESS_LOG
    enable_reload: bool = ENABLE_RELOAD


@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()
