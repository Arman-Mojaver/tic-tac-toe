import logging
from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "console": {
            "class": "config.logging_config.formatters.EnvFormatter",
            "format": "cli: %(asctime)s - %(environment)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "config.logging_config.handlers.ColorizingStreamHandler",
            "level": "DEBUG",
            "formatter": "console",
            "filters": [],
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "console",
            "filename": "logs/cli.log",
            "mode": "a",
            "maxBytes": 5 * 1024 * 1024,  # 5 MB
            "backupCount": 3,
        },
    },
    "filters": {},
    "loggers": {
        "custom_logger": {"level": "DEBUG", "handlers": ["console", "file"]},
    },
    "root": {
        "level": "INFO",
    },
}

dictConfig(LOGGING_CONFIG)


log = logging.getLogger("custom_logger")
