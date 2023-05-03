from enum import Enum
from pydantic import BaseModel
from typing import TypeVar


Session = str
SessionList = list[Session]

ValueAgg = int

SessionID = str

Matches = int
Player = str
Players = list[Player]
Outsiders = Players
Winner = Player | None
Move = Player | None

ErrorType = str
ErrorMsg = str

SelectiveState = TypeVar(
    "SelectiveState",
    Matches,
    Players,
    Outsiders,
    Player,
    Winner,
    Move
)


class RootQueryAgg(str, Enum):
    count = "count"


class RootQueryStatus(str, Enum):
    active = "active"
    wait = "wait"


class RequestSelectState(str, Enum):
    matches = "matches"
    players = "players"
    outsiders = "outsiders"
    winner = "winner"
    move = "move"


class ResponseAggSessions(BaseModel):
    value: ValueAgg


class ResponseSessions(BaseModel):
    sessions: SessionList


class RequestCreateSession(BaseModel):
    session_id: SessionID
    players: Players

    class Config:
        schema_extra = {
            "example": {
                "session_id": "12345",
                "players": ["SciBourne", "Leeroy", "Shepard"]
            }
        }


class RequestLeavePlayer(BaseModel):
    leave: Player

    class Config:
        schema_extra = {
            "example": {
                "leave": "Leeroy"
            }
        }


class RequestMakeMove(BaseModel):
    take: Matches

    class Config:
        schema_extra = {
            "example": {
                "take": 3
            }
        }


class ResponseSelectStateSession(BaseModel):
    value: SelectiveState


class ResponseStateSession(BaseModel):
    players: Players
    outsiders: Outsiders
    winner: Winner
    move: Player
    matches: Matches

    class Config:
        schema_extra = {
            "example": {
                "players": ["SciBourne", "Leeroy", "Shepard"],
                "outsiders": [],
                "winner": None,
                "move": "SciBourne",
                "matches": 33
            }
        }


class ResponseError(BaseModel):
    error_type: ErrorType
    error_msg: ErrorMsg

    class Config:
        schema_extra = {
            "example": {
                "error_type": "RuntimeError",
                "error_msg": "You cannot restart the game"
            }
        }
