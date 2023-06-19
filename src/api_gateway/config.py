import sys
from enum import Enum
from functools import wraps
from typing import Callable, Annotated

from fastapi import FastAPI
from hypercorn.config import Config as HypercornConfig


GW_TITLE: str = "API Gateway [ Spichki Game ]"

GW_REST_PREFIX: str = "/api"
GW_WS_PREFIX: str = "/ws"

GW_DESCRIPTION = (
    "<br> \n"
    "<br> \n"
    "<br> \n"

    "## Gateway mountpoints \n"

    "| Mountpoint name | Link | Documentation version | \n"
    "|---|---|---| \n"

    "| `REST API` |"
    f"[ {GW_REST_PREFIX}/v1/docs ]({GW_REST_PREFIX}/v1/docs)"
    "| OpenAPI | \n"

    "| `WebSocket API` |"
    f"[{GW_WS_PREFIX}/v1/docs]({GW_WS_PREFIX}/v1/docs)"
    "| AsyncAPI | \n"

    "<br> \n"
    "<br> \n"
    "<br> \n"

    "## Arch scheme \n"
    "![Gateway Arch](img/gateway_arch.png)"
)


class ServerConfigBuilder:
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

    def __new__(cls, **kwargs) -> HypercornConfig:
        cls.__init__(config := HypercornConfig(), **kwargs)
        return config


class GatewayBuilder:
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
            ]    ):

        self.title = title
        self.description = description

        self.mount(*rest_api_mountpoint)
        self.mount(*ws_api_mountpoint)

    def __new__(cls, **kwargs) -> FastAPI:
        cls.__init__(gateway := FastAPI(), **kwargs)
        return gateway


class EnumArgvOption(str, Enum):
    secure_connection = "--secure_connection"

    host = "--host"
    port = "--port"

    sertfile = "--certfile"
    keyfile = "--keyfile"


def command_line_argv(start_func: Callable) -> Callable:
    @wraps(start_func)
    def wrapper(**parameters) -> Callable:
        if len(sys.argv) != 1:
            for option_key, option_value in (sys.argv[1::2], sys.argv[2::2]):
                match option_key:

                    case EnumArgvOption.secure_connection:
                        parameters.update(
                            secure_connection=option_value
                        )

                    case EnumArgvOption.host:
                        parameters.update(
                            host=option_value
                        )

                    case EnumArgvOption.port:
                        parameters.update(
                            port=option_value
                        )

                    case EnumArgvOption.sertfile:
                        parameters.update(
                            certfile=option_value
                        )

                    case EnumArgvOption.keyfile:
                        parameters.update(
                            keyfile=option_value
                        )

        return start_func(**parameters)
    return wrapper
