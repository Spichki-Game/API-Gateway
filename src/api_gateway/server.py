import asyncio

from fastapi.staticfiles import StaticFiles
from hypercorn.asyncio import serve as hypercorn_serve

from api_gateway.versioner import VersionedFastAPI, EnumProto
from api_gateway.service_manager import ServiceManager
from api_gateway.logger import log

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

# TODO: Hypercorn config.yaml
# TODO: API Gateway config.yaml
# TODO: ServiceManager config.yaml
# TODO: Versioner config.yml

# TODO: Registry Service
# TODO: Router Service

# TODO: Controller HTTP -- gRPC
# TODO: Controller WebSocket -- gRPC

# TODO: Dynamic update routers
# TODO: Dynamic update configs


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
        secure_connection=secure_connection,
        host=host,
        port=port,
        sertfile=sertfile,
        keyfile=keyfile
    )

    service_pool = ServiceManager(
        registry_addr="127.0.0.1:6310",
        auto_update=True,
        time_step="15 sec"
    )

    api_gateway = GatewayBuilder(
        title=GW_TITLE,
        description=GW_DESCRIPTION,

        rest_api_mountpoint=(
            GW_REST_PREFIX,

            VersionedFastAPI(
                app=service_pool.router.http,
                proto=EnumProto.http
            )
        ),

        ws_api_mountpoint=(
            GW_WS_PREFIX,

            VersionedFastAPI(
                app=service_pool.router.websocket,
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
        "Hypercorn server starting on "

        f"http{'s' if secure_connection else ''}://"
        f"{host}:{port}"
    )

    log.info(
        "API Gateway documentation: "
        f"http{'s' if secure_connection else ''}://"
        f"{host}:{port}/docs"
    )

    asyncio.gather(

        service_pool.updater(
            gateway=api_gateway
        ),

        hypercorn_serve(
            app=api_gateway,
            config=server_config
        )

    )
