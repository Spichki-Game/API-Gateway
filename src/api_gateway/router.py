import os

from fastapi import FastAPI, APIRouter, Response
from fastapi_versioning import version

from api_gateway.logger import log

from api_gateway.docs import (
    websocket_docs,
    COMMON_DESCRIPTION
)

from api_gateway.versioner import (
    EnumStateAPI,
    PREFIX_API_VERSION,
    LATEST_API_VERSION
)


class ServiceManager:
    SERVICE_PACKAGE = "handlers"
    SERVICE_PATH = "src/handlers"

    def __init__(self):
        self.service_names: list[str] = []
        self.http_routers: list[APIRouter] = []
        self.websocket_routers: list[APIRouter] = []

    def import_routers(self, srv_name: str) -> bool:
        module_import = f"from {self.SERVICE_PACKAGE}.{srv_name}"
        names_import = ["http_router", "websocket_router"]
        aliases = [f"{srv_name}_{name}" for name in names_import]

        for name, alias in zip(names_import, aliases):
            code_body = (
                f"{module_import} import {name} as {alias} \n"
                f"self.{name}s.append({alias})"
            )

            try:
                exec(code_body)
                log.success(f"{alias} imported")
                return True

            except ImportError:
                log.error(f"{alias} cannot be imported")
                return False

    def scan(self):
        log.info(f"Service directory: {self.SERVICE_PATH}/")

        service_names = os.listdir(self.SERVICE_PATH)

        for srv_name in service_names:
            log.info(f"-> find service: {srv_name}")

        for srv_name in service_names:
            if self.import_routers(srv_name):
                self.service_names.append(srv_name)

        if self.service_names:
            for srv_name in self.service_names:
                log.success(f"-> valid service: {srv_name}")
        else:
            log.warning("Not valid services")

        log.info(f"-> HTTP routers: {self.http_routers}")
        log.info(f"-> WebSocket routers: {self.websocket_routers}")

        if not self.http_routers and not self.websocket_routers:
            log.warning("Not available routers")


class RouterManager:
    def __init__(self):
        self.service_manager = ServiceManager()

        self.http = FastAPI(
            title="REST API Gateway [ Spichki Game ]",
            description=COMMON_DESCRIPTION
        )

        self.websocket = FastAPI(
            title="WebSocket API Gateway [ Spichki Game ]",
            docs_url=None,
            redoc_url=None,
            description=COMMON_DESCRIPTION
        )

        websocket_docs(
            app=self.websocket,
            asyncapi_path="/asyncapi.json",
            docs_path="/docs"
        )

        self.__version_status(
            app=self.http,
            api_version=1,
            status="Actual"
        )

        self.__version_status(
            app=self.websocket,
            api_version=1,
            status="Actual"
        )

    def __version_status(self,
                         app: FastAPI,
                         api_version: int,
                         status: EnumStateAPI) -> None:

        @app.head('/', tags=["Root"], summary="Check API state")
        @version(api_version)
        async def check_api_state():
            return Response(
                headers={
                    "Current-API-Version": status,
                    "Latest-API-Version": (f"{PREFIX_API_VERSION}"
                                           f"{LATEST_API_VERSION}")
                }
            )

    def scan_services(self):
        self.service_manager.scan()
