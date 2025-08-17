import hashlib


class InfoHash:
    @staticmethod
    def get_info_hash(info_bytes: bytes) -> bytes:
        return hashlib.sha1(info_bytes).digest()
