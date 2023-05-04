from dataclasses import field
from typing import List, Optional, ClassVar, Type

from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE

@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: str
    username: str
    last_name: Optional[str] = ''
    language_code: Optional[str] = 'en'

    class Meta:
        unknown = EXCLUDE

@dataclass
class Chat: 
    id: int
    first_name: str
    last_name: str
    username: str
    type: str


@dataclass
class Message:
    message_id: int
    from_: MessageFrom =  field(metadata={'data_key': 'from'})
    chat: Chat
    date: int
    text: Optional[str] = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Message

    class Meta:
        unknown = EXCLUDE

@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE
