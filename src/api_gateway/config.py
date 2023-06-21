import sys
from enum import Enum
from functools import wraps
from typing import Callable, Annotated

from fastapi import FastAPI
from hypercorn.config import Config as HypercornConfig


GW_REST_PREFIX = "/api"
GW_WS_PREFIX = "/ws"


class ServerConfigBuilder(HypercornConfig):
    def __init__(self,
                 secure_connection: bool,
                 host: str,
                 port: str,
                 sertfile: str,
                 keyfile: str):

        if secure_connection:
            self.certfile = sertfile
            self.keyfile = keyfile
        else:
            self.bind = f"{host}:{port}"

        self.loglevel = "INFO"
        self.access_log_format = "%(m)s: HTTP %(H)s %(h)s%(Uq)s %(s)s %(st)s"

        self.accesslog = "logs/hypercorn_access.log"
        self.errorlog = "logs/hypercorn_error.log"

    def __new__(cls, **kwargs) -> HypercornConfig:
        cls.__init__(config := HypercornConfig(), **kwargs)
        return config


class GatewayBuilder(FastAPI):
    def __init__(

            self,

            title: Annotated[
                str, "Gateway name for docs"
            ],

            description: Annotated[
                str, "Gateway description for docs"
            ],

            rest_api_mountpoint: Annotated[
                tuple[str, FastAPI],
                "HTTP mountpoint for FastAPI application: (prefix, app)",
                ("/api", FastAPI)
            ],

            ws_api_mountpoint: Annotated[
                tuple[str, FastAPI],
                "WebSocket mountpoint for FastAPI application: (prefix, app)",
                ("/ws", FastAPI)
            ]

    ):

        self.title = title
        self.description = description

        self.mount(*rest_api_mountpoint)
        self.mount(*ws_api_mountpoint)

    def __new__(cls, **kwargs) -> FastAPI:
        cls.__init__(gateway := FastAPI(), **kwargs)
        return gateway


class EnumArgvOption(str, Enum):
    secure_connection = "--secure-connection"
    host = "--host"
    port = "--port"
    sertfile = "--certfile"
    keyfile = "--keyfile"


def command_line_argv(start_func: Callable) -> Callable:
    @wraps(start_func)
    def wrapper(**parameters) -> Callable:
        if len(sys.argv) > 1:
            keys = [
                key[2:].replace('-', '_') for key in [
                    EnumArgvOption(opt) for opt in sys.argv[1::2]
                ]
            ]

            values = sys.argv[2::2]
            parameters = dict(zip(keys, values))

        return start_func(**parameters)
    return wrapper
