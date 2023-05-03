from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
STATE_ALL: EnumState
STATE_MATCHES: EnumState
STATE_MOVE: EnumState
STATE_OUTSIDERS: EnumState
STATE_PLAYERS: EnumState
STATE_UNSPECIFIED: EnumState
STATE_WINNER: EnumState

class Game(_message.Message):
    __slots__ = ["session_id"]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class Matches(_message.Message):
    __slots__ = ["number", "session_id"]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    number: int
    session_id: str
    def __init__(self, session_id: _Optional[str] = ..., number: _Optional[int] = ...) -> None: ...

class Player(_message.Message):
    __slots__ = ["name", "session_id"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    session_id: str
    def __init__(self, session_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class Players(_message.Message):
    __slots__ = ["names", "session_id"]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ..., names: _Optional[_Iterable[str]] = ...) -> None: ...

class RequestState(_message.Message):
    __slots__ = ["codes", "session_id"]
    CODES_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    codes: _containers.RepeatedScalarFieldContainer[EnumState]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ..., codes: _Optional[_Iterable[_Union[EnumState, str]]] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["confirm_status", "error_body", "state_body"]
    CONFIRM_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_BODY_FIELD_NUMBER: _ClassVar[int]
    STATE_BODY_FIELD_NUMBER: _ClassVar[int]
    confirm_status: bool
    error_body: ResponseError
    state_body: ResponseState
    def __init__(self, confirm_status: bool = ..., state_body: _Optional[_Union[ResponseState, _Mapping]] = ..., error_body: _Optional[_Union[ResponseError, _Mapping]] = ...) -> None: ...

class ResponseError(_message.Message):
    __slots__ = ["error_msg", "error_type"]
    ERROR_MSG_FIELD_NUMBER: _ClassVar[int]
    ERROR_TYPE_FIELD_NUMBER: _ClassVar[int]
    error_msg: str
    error_type: str
    def __init__(self, error_type: _Optional[str] = ..., error_msg: _Optional[str] = ...) -> None: ...

class ResponseState(_message.Message):
    __slots__ = ["codes", "matches", "move", "outsiders", "players", "winner"]
    CODES_FIELD_NUMBER: _ClassVar[int]
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    MOVE_FIELD_NUMBER: _ClassVar[int]
    OUTSIDERS_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    WINNER_FIELD_NUMBER: _ClassVar[int]
    codes: _containers.RepeatedScalarFieldContainer[EnumState]
    matches: int
    move: str
    outsiders: _containers.RepeatedScalarFieldContainer[str]
    players: _containers.RepeatedScalarFieldContainer[str]
    winner: str
    def __init__(self, matches: _Optional[int] = ..., move: _Optional[str] = ..., winner: _Optional[str] = ..., players: _Optional[_Iterable[str]] = ..., outsiders: _Optional[_Iterable[str]] = ..., codes: _Optional[_Iterable[_Union[EnumState, str]]] = ...) -> None: ...

class EnumState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
