import asyncio

from fastapi import FastAPI, Response, Request
from fastapi_versioning import VersionedFastAPI, version

from hypercorn.config import Config
from hypercorn.asyncio import serve

from routers import game_scene


VERSION_API_FORMAT = "{major}"
PREFIX_API_VERSION = "/api/v"
LATEST_API_VERSION = 1

api_gateway = FastAPI(title="API Gateway [ Spichki Game ]")


@api_gateway.head('/',
                  tags=["Root"],
                  summary="Check API state")
@version(1)
async def head_check_api_state():
    return Response(
        headers={
            "Current-API-Version": "Actual",
            "Latest-API-Version": (f"{PREFIX_API_VERSION}"
                                   f"{LATEST_API_VERSION}")
        }
    )


@api_gateway.get('/',
                 tags=["Root"],
                 summary="Check API state")
@version(1)
async def get_check_api_state():
    return {"current-api-version": "actual",
            "latest-api-version": (f"{PREFIX_API_VERSION}"
                                   f"{LATEST_API_VERSION}")}


def start() -> None:
    api_gateway.include_router(
        game_scene.router
    )

    app = VersionedFastAPI(
        api_gateway,
        version_format=VERSION_API_FORMAT,
        prefix_format=f"{PREFIX_API_VERSION}{LATEST_API_VERSION}",
        default_api_version=LATEST_API_VERSION
    )

    asyncio.run(
        serve(app, Config())
    )
