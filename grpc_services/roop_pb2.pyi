from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RoopInputMsg(_message.Message):
    __slots__ = ("source", "target", "processor", "reference_face_position", "dest")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    PROCESSOR_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FACE_POSITION_FIELD_NUMBER: _ClassVar[int]
    DEST_FIELD_NUMBER: _ClassVar[int]
    source: str
    target: str
    processor: str
    reference_face_position: int
    dest: str
    def __init__(self, source: _Optional[str] = ..., target: _Optional[str] = ..., processor: _Optional[str] = ..., reference_face_position: _Optional[int] = ..., dest: _Optional[str] = ...) -> None: ...

class RoopResponse(_message.Message):
    __slots__ = ("result", "dest")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    DEST_FIELD_NUMBER: _ClassVar[int]
    result: bool
    dest: str
    def __init__(self, result: bool = ..., dest: _Optional[str] = ...) -> None: ...
