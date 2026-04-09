import json
import logging
import sys
from datetime import datetime, timezone
from logging.config import dictConfig

from app.core import Settings, get_settings


class JsonFormatter(logging.Formatter):
    """
    Simple structured JSON log formatter.
    Docker-ready (stdout).
    """

    def __init__(self, environment: str) -> None:
        super().__init__()
        self.env: str = environment

    def format(self, record: logging.LogRecord) -> str:
        log_record: dict[str, str] = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'environment': self.env,
        }

        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_record)


def configure_logging() -> None:
    """
    Configure global logging for the application.
    Must be called before FastAPI app initialization.
    """

    settings: Settings = get_settings()

    dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'json': {
                    '()': JsonFormatter,
                    'environment': settings.environment,
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'stream': sys.stdout,
                    'formatter': 'json',
                }
            },
            'root': {
                'level': settings.log_level,
                'handlers': ['console'],
            },
            'loggers': {
                'uvicorn': {
                    'handlers': ['console'],
                    'level': settings.log_level,
                    'propagate': False,
                },
                'uvicorn.error': {
                    'handlers': ['console'],
                    'level': settings.log_level,
                    'propagate': False,
                },
                'uvicorn.access': {
                    'handlers': ['console'],
                    'level': settings.log_level,
                    'propagate': False,
                },
            },
        }
    )
