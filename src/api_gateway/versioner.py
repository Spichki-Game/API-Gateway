from enum import Enum

from fastapi import FastAPI, Response
from fastapi_versioning import VersionedFastAPI as TempVersionedFastAPI
from fastapi_versioning import version

from api_gateway.router import http_router


VERSION_API_FORMAT = "{major}"
PREFIX_API_VERSION = "/v"
LATEST_API_VERSION = 1


class EnumProto(str, Enum):
    http = "HTTP"
    websocket = "WebSocket"


class EnumStateAPI(str, Enum):
    actual = "Actual"
    deprecated = "Deprecated"


# TODO: Wait fix fastapi_versioning for WebSocket
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


@http_router.head('/', tags=["Root"], summary="Check API state")
@version(1)
async def check_api_state():
    return Response(
        headers={
            "Current-API-Version": EnumStateAPI.actual,
            "Latest-API-Version": (f"{PREFIX_API_VERSION}"
                                   f"{LATEST_API_VERSION}")
        }
    )
