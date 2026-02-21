import logging
import logging.config


logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standart": {
            "format": "{asctime} - {levelname} - {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standart",
            "level": "INFO",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standart",
            "filename": "logs/logs.log",
            "maxBytes": 10485760,
            "backupCount": 5,
            "encoding": "utf-8",
            "level": "WARNING",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}


def setting_logging(config: dict) -> None:

    logging.config.dictConfig(config)
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
