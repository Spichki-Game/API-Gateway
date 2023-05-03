from functools import wraps
from fastapi import status
from fastapi.responses import JSONResponse
from typing import Any, Callable

from grpc_api import game_scene_pb2 as msg
from schemas import game_scene as scheme


def __response_deserialize(
        state_content: Any,
        raw_response: msg.Response
) -> tuple[bool, dict[str, Any] | None]:

    body: dict[str, Any] | None = {}

    if raw_response.confirm_status:
        state = raw_response.state_body

        match state_content:
            case msg.STATE_ALL:
                body.update(
                    players=list(state.players),
                    outsiders=list(state.outsiders),
                    winner=state.winner if state.winner else None,
                    move=state.move if state.move else None,
                    matches=state.matches
                )

            case msg.STATE_PLAYERS:
                body.update(
                    value=list(state.players)
                )

            case msg.STATE_OUTSIDERS:
                body.update(
                    value=list(state.outsiders)
                )

            case msg.STATE_WINNER:
                body.update(
                    value=state.winner if state.winner else None
                )

            case msg.STATE_MOVE:
                body.update(
                    value=state.move if state.move else None
                )

            case msg.STATE_MATCHES:
                body.update(
                    value=state.matches
                )
    else:
        body.update(
            error_type=raw_response.error_body.error_type,
            error_msg=raw_response.error_body.error_msg
        )

    return raw_response.confirm_status, body


def __response_validate(body, state_content=None):
    if state_content:
        if state_content == msg.STATE_ALL:
            scheme.ResponseStateSession(**body)
        else:
            scheme.ResponseSelectStateSession(**body)
    else:
        scheme.ResponseError(**body)


async def __post_handler(

        call_next: Callable,
        request: scheme.RequestCreateSession

) -> JSONResponse:

    state_content, raw_response = await call_next(request)
    confirm, body = __response_deserialize(state_content, raw_response)

    if confirm:
        __response_validate(body, state_content)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            headers={"Location": request.session_id},
            content=body
        )

    else:
        __response_validate(body)

        return JSONResponse(
            status_code=status.HTTP_423_LOCKED,
            content=body
        )


async def __patch_handler(

        call_next: Callable,
        session_id: scheme.SessionID,
        request: scheme.RequestMakeMove | scheme.RequestLeavePlayer

) -> JSONResponse:

    state_content, raw_response = await call_next(session_id, request)
    confirm, body = __response_deserialize(state_content, raw_response)

    if confirm:
        __response_validate(body, state_content)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=body
        )

    else:
        __response_validate(body)

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=body
        )


async def __get_state_handler(

        call_next: Callable,
        session_id: str

) -> JSONResponse:

    state_content, raw_response = await call_next(session_id)
    confirm, body = __response_deserialize(state_content, raw_response)

    if confirm:
        __response_validate(body, state_content)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=body
        )

    else:
        __response_validate(body)

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=body
        )


async def __get_parameter_handler(

        call_next: Callable,
        session_id: str,
        state_parameter: scheme.RequestSelectState

) -> JSONResponse:

    state_content, raw_response = await call_next(session_id, state_parameter)
    confirm, body = __response_deserialize(state_content, raw_response)

    if confirm:
        __response_validate(body, state_content)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=body
        )

    else:
        __response_validate(body)

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=body
        )


async def __delete_handler(

        call_next: Callable,
        session_id: str

) -> JSONResponse:

    state_content, raw_response = await call_next(session_id)
    confirm, body = __response_deserialize(state_content, raw_response)

    if confirm:

        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content=None
        )

    else:
        __response_validate(body)

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=body
        )


def response_handler(tag: str) -> Callable:
    def decorator(call_next: Callable) -> Callable:
        @wraps(call_next)
        async def dispatch(*args, **kwargs) -> JSONResponse:
            handler: Callable

            match tag:
                case "POST":
                    handler = __post_handler
                case "PATCH":
                    handler = __patch_handler
                case "GET state":
                    handler = __get_state_handler
                case "GET parameter":
                    handler = __get_parameter_handler
                case "DELETE":
                    handler = __delete_handler

            return await handler(call_next, *args, **kwargs)

        return dispatch
    return decorator
