import logging
import logging.config
from logging import Logger
from typing import Any

import coloredlogs


class ColoredExtraFormatter(coloredlogs.ColoredFormatter):
    def format(self, record):
        # Get the base colored message
        base_message = super().format(record)

        # Add extra fields if they exist
        extra_fields = []
        for key, value in record.__dict__.items():
            if key not in [
                'name',
                'msg',
                'args',
                'levelname',
                'levelno',
                'pathname',
                'filename',
                'module',
                'lineno',
                'funcName',
                'created',
                'msecs',
                'relativeCreated',
                'thread',
                'threadName',
                'processName',
                'process',
                'getMessage',
                'exc_info',
                'exc_text',
                'stack_info',
                'asctime',
                'hostname',
                'message',
                'taskName',
            ]:
                extra_fields.append(f"{key}={value}")

        if extra_fields:
            return f"{base_message} [{', '.join(extra_fields)}]"
        return base_message


UVICORN_LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": ColoredExtraFormatter,  # Use the class directly, not string reference
            "fmt": "%(asctime)s %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s",
        },
        "access": {
            "()": coloredlogs.ColoredFormatter,
            "fmt": "%(asctime)s %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s",
        },
    },
    "filters": {
        "hostname": {
            "()": coloredlogs.HostNameFilter,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "filters": ["hostname"],
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": ["hostname"],
        },
    },
    "loggers": {
        "": {"handlers": ["default"], "level": "DEBUG", "propagate": False},
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {
            "handlers": ["access"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

# Configure logging
logging.config.dictConfig(UVICORN_LOGGING_CONFIG)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

logger: Logger = logging.getLogger(__name__)
