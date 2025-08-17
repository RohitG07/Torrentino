from enum import Enum


class MessageType(Enum):
    KEEP_ALIVE = 0
    CHOKE = 1
    UNCHOKE = 2
    INTERESTED = 3
    NOT_INTERESTED = 4
    HAVE = 5
    BITFIELD = 6
    REQUEST = 7
    PIECE = 8
    CANCEL = 9

    @classmethod
    def from_value(cls, value: int) -> "MessageType":
        for msg_type in cls:
            if msg_type.value == value:
                return msg_type
        raise ValueError(f"Invalid MessageType value: {value}")
