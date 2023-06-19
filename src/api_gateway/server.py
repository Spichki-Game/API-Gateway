import asyncio
from fastapi.staticfiles import StaticFiles
from hypercorn.asyncio import serve as hypercorn_serve

from api_gateway.versioner import VersionedFastAPI, EnumProto
from api_gateway.router import http_router, websocket_router

from api_gateway.config import (
    ServerConfigBuilder,
    GatewayBuilder,
    command_line_argv
)

from api_gateway.config import (
    GW_TITLE,
    GW_REST_PREFIX,
    GW_WS_PREFIX,
    GW_DESCRIPTION
)


@command_line_argv
def start(

        *,
        secure_connection: bool = False,

        host: str = "localhost",
        port: str = "8000",

        sertfile: str = ".ssl/cert.pem",
        keyfile: str = ".ssl/key.pem"

) -> None:

    server_config = ServerConfigBuilder(
        **locals()
    )

    api_gateway = GatewayBuilder(
        title=GW_TITLE,
        description=GW_DESCRIPTION,

        rest_api_mountpoint=(
            GW_REST_PREFIX,

            VersionedFastAPI(
                app=http_router,
                proto=EnumProto.http
            )
        ),

        ws_api_mountpoint=(
            GW_WS_PREFIX,

            VersionedFastAPI(
                app=websocket_router,
                proto=EnumProto.websocket
            )
        )
    )

    api_gateway.mount(
        "/img",
        StaticFiles(directory="img")
    )

    asyncio.run(
        hypercorn_serve(api_gateway, server_config)
    )
