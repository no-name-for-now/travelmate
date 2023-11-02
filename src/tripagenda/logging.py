import os


LOGGER_NAME: str = "tripagenda"
LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOGGER_VERSION = "1.0.0"

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    },
}
