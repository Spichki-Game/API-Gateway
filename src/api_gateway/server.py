import asyncio
from typing import Any

from api_gateway.exceptions import ConfigUpdated, ServiceUpdated
from api_gateway.config import command_line_argv
from api_gateway.managers import GatewayManager

from api_gateway.logger import log


async def gateway_event_loop(server_options: dict[str, Any]) -> None:
    gateway = GatewayManager(
        server_options=server_options
    )

    while True:
        try:
            async with asyncio.TaskGroup() as group:
                group.create_task(
                    gateway.run()
                )

                group.create_task(
                    gateway.config_watcher()
                )

                group.create_task(
                    gateway.service_watcher()
                )

        except ConfigUpdated:
            if gateway.rebuild():
                log.success(
                    "API Gateway configuration updated"
                )

            else:
                log.warning(
                    "API Gateway configuration has some problems, "
                    "updating is not possible"
                )

        except ServiceUpdated:
            if gateway.rebuild():
                log.success(
                    "Service pool routes updated"
                )

            else:
                log.warning(
                    "Something in the pool of services has some problems, "
                    "updating is not possible"
                )


@command_line_argv
def start(

        *,

        host: str | None = None,
        port: str | None = None,

        secure_connection: bool | None = None,

        sertfile: str | None = None,
        keyfile: str | None = None

) -> None:

    asyncio.run(
        gateway_event_loop(
            server_options=locals()
        )
    )
