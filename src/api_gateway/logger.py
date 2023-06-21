import os
import sys

from typing import Annotated

from loguru import logger
from loguru._logger import Logger


log: Annotated[Logger, "loguru logger instance"] = logger
log: Logger


LEVEL: str = os.getenv("LOG_LEVEL") or "INFO"
LEVEL_LOGFILE: str = "DEBUG"

ROTATION_LOGFILE: str | int = "100 MB"
RETENTION_LOGFILE: int = 2

PATH_OUTFILE: str = "logs/api_gateway.log"


log.remove(handler_id=0)

log.add(
    sink=sys.stderr,
    level=LEVEL
)

log.add(
    sink=PATH_OUTFILE,
    level=LEVEL_LOGFILE,
    serialize=True,
    rotation=ROTATION_LOGFILE,
    retention=RETENTION_LOGFILE,
    delay=True
)


log.success("Logger configured")
log.success("Start logging")
