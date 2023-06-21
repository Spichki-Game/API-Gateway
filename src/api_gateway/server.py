import os
import asyncio

from fastapi.staticfiles import StaticFiles
from hypercorn.asyncio import serve as hypercorn_serve

from api_gateway.versioner import VersionedFastAPI, EnumProto
from api_gateway.router import RouterManager
from api_gateway.logger import LoggerBuilder

from api_gateway.config import (
    ServerConfigBuilder,
    GatewayBuilder,
    command_line_argv,
    GW_REST_PREFIX,
    GW_WS_PREFIX
)

from api_gateway.docs import (
    GW_TITLE,
    GW_DESCRIPTION
)


log = LoggerBuilder(
    level=os.getenv("LOG_LEVEL")
)


@log.catch
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

    router = RouterManager()
    router.scan_services()

    api_gateway = GatewayBuilder(
        title=GW_TITLE,
        description=GW_DESCRIPTION,

        rest_api_mountpoint=(
            GW_REST_PREFIX,

            VersionedFastAPI(
                app=router.http,
                proto=EnumProto.http
            )
        ),

        ws_api_mountpoint=(
            GW_WS_PREFIX,

            VersionedFastAPI(
                app=router.websocket,
                proto=EnumProto.websocket
            )
        )
    )

    api_gateway.mount(
        "/img", StaticFiles(directory="img")
    )

    log.success(
        "API Gateway is ready"
    )

    log.info(
        "Hypercorn will be starting at "

        f"http{'s' if secure_connection else ''}://"
        f"{host}:{port}"
    )

    log.info(
        "API Gateway documentation: "
        f"http{'s' if secure_connection else ''}://"
        f"{host}:{port}/docs"
    )

    asyncio.run(
        hypercorn_serve(api_gateway, server_config)
    )
