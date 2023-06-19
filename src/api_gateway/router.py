from fastapi import FastAPI
from api_gateway.docs import asyncapi_json, asyncapi_docs


http_router = FastAPI(
    title="REST API Gateway [ Spichki Game ]"
)

websocket_router = FastAPI(
    title="WebSocket API Gateway [ Spichki Game ]",
    docs_url=None,
    redoc_url=None
)


websocket_router.add_api_route(
    methods=["GET"],
    path="/asyncapi.json",
    endpoint=asyncapi_json(websocket_router),
    include_in_schema=False
)

websocket_router.add_api_route(
    methods=["GET"],
    path="/docs",
    endpoint=asyncapi_docs(websocket_router),
    include_in_schema=False
)
