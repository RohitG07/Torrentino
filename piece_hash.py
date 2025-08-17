from typing import List


class PieceHash:
    @staticmethod
    def get_piece_hash(piece_hash: bytes, piece_length: int) -> List[bytes]:
        piece_hash_list = []
        for i in range(0, len(piece_hash), piece_length):
            piece_hash_list.append(piece_hash[i:i+piece_length])
        return piece_hash_list
