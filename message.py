from typing import Optional
from message_type import MessageType


class Message:
    def __init__(self, type_or_value, payload: Optional[bytes] = None):
        if isinstance(type_or_value, MessageType):
            self.type = type_or_value
        elif isinstance(type_or_value, int):
            self.type = MessageType.from_value(type_or_value)
        else:
            raise ValueError(f"Invalid type: {type_or_value}")

        self.payload = payload or b""

    def get_type(self) -> MessageType:
        return self.type

    def get_payload(self) -> bytes:
        return self.payload
