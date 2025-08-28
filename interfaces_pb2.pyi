from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserCredentials(_message.Message):
    __slots__ = ["login_button_id", "password", "password_input_id", "root_url", "username", "username_input_id"]
    LOGIN_BUTTON_ID_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_INPUT_ID_FIELD_NUMBER: _ClassVar[int]
    ROOT_URL_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    USERNAME_INPUT_ID_FIELD_NUMBER: _ClassVar[int]
    login_button_id: str
    password: str
    password_input_id: str
    root_url: str
    username: str
    username_input_id: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ..., root_url: _Optional[str] = ..., login_button_id: _Optional[str] = ..., username_input_id: _Optional[str] = ..., password_input_id: _Optional[str] = ...) -> None: ...
