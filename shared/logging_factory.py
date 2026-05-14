import logging
import json
from datetime import datetime
from typing import Any, Dict

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_payload = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "logger": record.name,
            "level": record.levelname,
            "event": record.msg,
        }
        if record.args and isinstance(record.args, dict):
            log_payload.update(record.args)
        return json.dumps(log_payload)

def get_structured_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger