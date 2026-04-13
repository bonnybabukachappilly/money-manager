import json
import logging
import sys
from datetime import datetime, timezone
from logging.config import dictConfig

from app.core import Settings, get_settings


class JsonFormatter(logging.Formatter):
    def __init__(self, environment: str) -> None:
        super().__init__()
        self.env: str = environment

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
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
    settings: Settings = get_settings()

    formatter_to_use = 'json' if settings.environment == 'production' else 'standard'

    dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'json': {
                    '()': JsonFormatter,
                    'environment': settings.environment,
                },
                'standard': {
                    'format': '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S',
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'stream': sys.stdout,
                    'formatter': formatter_to_use,  # Dynamically switched
                }
            },
            'root': {
                'level': settings.log_level,
                'handlers': ['console'],
            },
            'loggers': {
                'uvicorn': {
                    'level': 'INFO',
                    'handlers': ['console'], 'propagate': False
                },
                'uvicorn.error': {
                    'level': 'INFO',
                    'handlers': ['console'], 'propagate': False
                },
                'uvicorn.access': {
                    'level': 'INFO',
                    'handlers': ['console'], 'propagate': False
                },
                # Reduce SQL noise
                'sqlalchemy.engine': {
                    'level': 'WARNING',
                    'handlers': ['console'], 'propagate': False
                },
            },
        }
    )
