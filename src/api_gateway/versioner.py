from enum import Enum

from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI as TempVersionedFastAPI


VERSION_API_FORMAT = "{major}"
PREFIX_API_VERSION = "/v"
LATEST_API_VERSION = 1


class EnumProto(str, Enum):
    http = "HTTP"
    websocket = "WebSocket"


class EnumStateAPI(str, Enum):
    actual = "Actual"
    deprecated = "Deprecated"


class VersionedFastAPI:
    def __init__(self, app: FastAPI, proto: EnumProto):
        pass

    def __new__(cls, app, proto) -> FastAPI:
        match proto:
            case "HTTP":
                return TempVersionedFastAPI(
                    app,
                    version_format=VERSION_API_FORMAT,
                    prefix_format=f"{PREFIX_API_VERSION}{VERSION_API_FORMAT}"
                )

            case "WebSocket":
                new_app = FastAPI()

                new_app.mount(
                    f"{PREFIX_API_VERSION}{LATEST_API_VERSION}",
                    app
                )

                return new_app
