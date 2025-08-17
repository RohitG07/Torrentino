from typing import List


class TorrentMetaData:
    def __init__(self, announce_url: str, piece_length: int, pieces: bytes, name: str, files: List["TorrentFile"]):
        self.announce_url = announce_url
        self.piece_length = piece_length
        self.pieces = pieces
        self.name = name
        self.files = files
        self.info_hash = None
        self.piece_hash = []

    def get_url(self) -> str:
        return self.announce_url

    def get_piece_length(self) -> int:
        return self.piece_length

    def get_pieces(self) -> bytes:
        return self.pieces

    def get_files(self) -> List["TorrentFile"]:
        return self.files

    def get_name(self) -> str:
        return self.name

    def get_info_hash(self) -> bytes:
        return self.info_hash

    def set_info_hash(self, info_hash: bytes):
        self.info_hash = info_hash

    def get_piece_hash(self) -> List[bytes]:
        return self.piece_hash

    def set_piece_hash(self, piece_hash: List[bytes]):
        self.piece_hash = piece_hash
