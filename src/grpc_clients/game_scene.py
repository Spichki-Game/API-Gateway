import grpc

from grpc_api import game_scene_pb2_grpc as srv
from grpc_api import game_scene_pb2 as msg


SERVICE_ADDR = "localhost:50000"


async def create_session(session_id: str, players: list[str]) -> tuple:
    async with grpc.aio.insecure_channel(SERVICE_ADDR) as channel:
        stub = srv.GameSceneStub(channel)

        raw_response: msg.Response = await stub.Start(
            msg.Players(
                session_id=session_id,
                names=players
            )
        )

        return msg.STATE_ALL, raw_response


async def leave_player(session_id: str, player: str) -> tuple:
    async with grpc.aio.insecure_channel(SERVICE_ADDR) as channel:
        stub = srv.GameSceneStub(channel)

        raw_response: msg.Response = await stub.Leave(
            msg.Player(
                session_id=session_id,
                name=player
            )
        )

        return msg.STATE_ALL, raw_response


async def make_move(session_id: str, num_matches: int) -> tuple:
    async with grpc.aio.insecure_channel(SERVICE_ADDR) as channel:
        stub = srv.GameSceneStub(channel)

        raw_response: msg.Response = await stub.Move(
            msg.Matches(
                session_id=session_id,
                number=num_matches
            )
        )

        return msg.STATE_ALL, raw_response


async def get_state(session_id: str) -> tuple:
    async with grpc.aio.insecure_channel(SERVICE_ADDR) as channel:
        stub = srv.GameSceneStub(channel)

        raw_response: msg.Response = await stub.Get(
            msg.RequestState(
                session_id=session_id,
                codes=[msg.STATE_ALL]
            )
        )

        return msg.STATE_ALL, raw_response


async def get_selective_state(session_id: str, state_parameter: str) -> tuple:
    async with grpc.aio.insecure_channel(SERVICE_ADDR) as channel:
        stub = srv.GameSceneStub(channel)
        state = eval(f"msg.STATE_{state_parameter.upper()}")

        raw_response: msg.Response = await stub.Get(
            msg.RequestState(
                session_id=session_id,
                codes=[state]
            )
        )

        return state, raw_response


async def close(session_id: str) -> tuple:
    async with grpc.aio.insecure_channel(SERVICE_ADDR) as channel:
        stub = srv.GameSceneStub(channel)

        raw_response: msg.Response = await stub.Stop(
            msg.Game(
                session_id=session_id
            )
        )

        return None, raw_response
