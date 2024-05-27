import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "uvicorn": {
            "()": "uvicorn.logging.AccessFormatter",
            "format": "%(asctime)s - %(client_addr)s - %(levelname)s - %(request_line)s - %(status_code)s",
            "use_colors": None,
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "default",
            "class": "logging.StreamHandler",
        },
        "uvicorn.access": {
            "level": "INFO",
            "formatter": "uvicorn",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "INFO",
        },
        "uvicorn": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["uvicorn.access"],
            "level": "INFO",
            "propagate": False,
        },
        "sqlalchemy": {
            "handlers": ["default"],
            "level": "WARNING",
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "handlers": ["default"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
    # TODO: Ahhh can't disable sqlalchemy logs :(
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine.Engine").setLevel(logging.WARNING)
