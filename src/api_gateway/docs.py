"""
When the fastapi_asyncapi is finished, this file
will be refactored or removed.

This is necessary to support the documentation of
WebSocket protocol endpoints.

"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse

from pydantic import AnyHttpUrl
from fastapi_asyncapi import get_asyncapi, get_asyncapi_html

from api_gateway.config import GW_REST_PREFIX, GW_WS_PREFIX


GW_TITLE: str = "API Gateway [ Spichki Game ]"

GW_DESCRIPTION = (
    "<br>"
    "<br>"
    "<br> \n"

    "## Gateway mountpoints \n"

    "| Mountpoint name | Link | Documentation version | \n"
    "|---|---|---| \n"

    "| `REST API` |"
    f"<a href='{GW_REST_PREFIX}/v1/docs' target='_self'>"
    f"         {GW_REST_PREFIX}/v1/docs </a>"
    "| OpenAPI | \n"

    "| `WebSocket API` |"
    f"<a href='{GW_WS_PREFIX}/v1/docs' target='_self'>"
    f"         {GW_WS_PREFIX}/v1/docs </a>"
    "| AsyncAPI | \n"

    "<br>"
    "<br>"
    "<br> \n"

    "## Backend scheme \n"

    "<a href='/img/gateway_arch.png' target=_blank>"
    "  <img src='/img/gateway_arch.png' alt='' loading=lazy>"
    "</a>"


    "<p align=center><b>© 2023, Samael Arts studio</b></p>"
)

COMMON_DESCRIPTION = (
    "<br>"
    "<br>"

    "<a href='/docs' target='_self'>"
    "  <b>Back to main</b>"
    "</a>"

    "<br>"
    "<br>"
    "<br>"

    "<a href='/img/gateway_arch.png' target=_blank>"
    "  <img src='/img/gateway_arch.png' width=50% alt='' loading=lazy>"
    "</a>"

    "<p align=left><b>© 2023, Samael Arts studio</b></p>"
)


def websocket_docs(

        app: FastAPI,
        asyncapi_path: str,
        docs_path: str

) -> None:

    @app.get(path=asyncapi_path, include_in_schema=False)
    async def asyncapi_json() -> JSONResponse:
        return get_asyncapi(
            title=app.title,
            description=app.description,
            version=app.version,
            routes=app.routes
        )

    @app.get(path=docs_path, include_in_schema=False)
    async def asyncapi_docs() -> HTMLResponse:
        asyncapi_url = AnyHttpUrl(
            url="asyncapi.json",
            scheme="http"
        )

        return get_asyncapi_html(
            asyncapi_url=asyncapi_url,
            title=app.title
        )
