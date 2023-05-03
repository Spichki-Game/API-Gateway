from fastapi import APIRouter, status
from fastapi_versioning import version

from schemas import game_scene as scheme
from middlewares.game_scene import response_handler
from grpc_clients import game_scene as grpc_client


router = APIRouter(
    prefix="/game-scenes",
    tags=["Game Scene"]
)


@router.get("/",
            summary="List of game sessions",
            response_model=(scheme.ResponseSessions |
                            scheme.ResponseAggSessions))
@version(1)
async def get_sessions(query_status: scheme.RootQueryStatus = None,
                       agg: scheme.RootQueryAgg = None,
                       limit: int = None):

    # TODO: Wait game-lobby service

    fake_sessions = ["001", "002", "003", "004", "005"]
    response = []

    match query_status:
        case scheme.RootQueryStatus.active:
            response += fake_sessions[:3]
        case scheme.RootQueryStatus.wait:
            response += fake_sessions[3:]
        case _:
            response += fake_sessions

    match agg:
        case scheme.RootQueryAgg.count:
            response = len(response)

    if agg:
        return scheme.ResponseAggSessions(
            value=response
        )

    else:
        return scheme.ResponseSessions(
            fake_sessions=response[:limit]
        )


@router.post(
    "/",
    summary="Create game session",
    status_code=status.HTTP_201_CREATED,
    response_model=scheme.ResponseStateSession,

    responses={
        status.HTTP_201_CREATED: {
            "model": scheme.ResponseStateSession,

            "headers": {
                "Location": {
                    "description": "Game session ID",
                    "type": "string"
                }
            }
        },

        status.HTTP_423_LOCKED: {
            "model": scheme.ResponseError,
        }
    }
)
@version(1)
@response_handler(tag="POST")
async def create_session(request: scheme.RequestCreateSession):
    return await grpc_client.create_session(
        request.session_id,
        request.players
    )


@router.patch(
    "/{session_id}/players",
    summary="Leave the player",
    status_code=status.HTTP_200_OK,
    response_model=scheme.ResponseStateSession,

    responses={
        status.HTTP_200_OK: {
            "model": scheme.ResponseStateSession
        },

        status.HTTP_404_NOT_FOUND: {
            "model": scheme.ResponseError
        }
    }
)
@version(1)
@response_handler(tag="PATCH")
async def leave_player(session_id: scheme.SessionID,
                       request: scheme.RequestLeavePlayer):

    return await grpc_client.leave_player(
        session_id,
        request.leave
    )


@router.patch("/{session_id}/matches",
              summary="Make move",
              response_model=scheme.ResponseStateSession)
@version(1)
@response_handler(tag="PATCH")
async def make_move(session_id: scheme.SessionID,
                    request: scheme.RequestMakeMove):

    return await grpc_client.make_move(
        session_id,
        request.take
    )


@router.get("/{session_id}",
            summary="Get state",
            response_model=scheme.ResponseStateSession)
@version(1)
@response_handler(tag="GET state")
async def get_state_session(session_id: scheme.SessionID):
    return await grpc_client.get_state(
        session_id
    )


@router.get("/{session_id}/{state_parameter}",
            summary="Get selective state",
            response_model=scheme.ResponseSelectStateSession)
@version(1)
@response_handler(tag="GET parameter")
async def get_matches_session(session_id: scheme.SessionID,
                              state_parameter: scheme.RequestSelectState):

    return await grpc_client.get_selective_state(
        session_id,
        state_parameter
    )


@router.delete(
    "/{session_id}",
    summary="Close the game session",
    status_code=status.HTTP_204_NO_CONTENT,

    responses={
        status.HTTP_204_NO_CONTENT: {},

        status.HTTP_404_NOT_FOUND: {
            "model": scheme.ResponseError
        }
    }
)
@version(1)
@response_handler(tag="DELETE")
async def close_session(session_id: scheme.SessionID):
    return await grpc_client.close(
        session_id
    )
