import sys

from loguru import logger
from loguru._logger import Logger


class LoggerBuilder(Logger):
    def __init__(self, level: str = "INFO"):
        self.remove(0)

        self.add(sink=sys.stderr, level=level)

        self.add(
            sink="logs/api_gateway.log",
            level=level,
            serialize=True,
            rotation="1 day",
            retention=1,
            delay=True
        )

        self.info("Logger configured")

    def __new__(cls, *args, **kwargs) -> Logger:
        cls.__init__(log := logger, *args, **kwargs)
        return log
