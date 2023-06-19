"""
When the fastapi_asyncapi is finished, this file
will be refactored or removed.

This is necessary to support the documentation of
WebSocket protocol endpoints.

"""

from typing import Coroutine

from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse

from pydantic import AnyHttpUrl
from fastapi_asyncapi import get_asyncapi, get_asyncapi_html


def asyncapi_json(app: FastAPI) -> Coroutine:
    async def endpoint() -> JSONResponse:
        return get_asyncapi(
            title=app.title,
            description=app.description,
            version=app.version,
            routes=app.routes
        )

    return endpoint


def asyncapi_docs(app: FastAPI) -> Coroutine:
    async def endpoint() -> HTMLResponse:
        asyncapi_url = AnyHttpUrl(
            url="asyncapi.json",
            scheme="http"
        )

        return get_asyncapi_html(
            asyncapi_url=asyncapi_url,
            title=app.title
        )

    return endpoint
