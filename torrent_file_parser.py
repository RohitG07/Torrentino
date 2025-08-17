import os
import bencodepy

from torrent_file import TorrentFile
from piece_hash import PieceHash
from info_hash import InfoHash
from torrent_metadata import TorrentMetaData


class TorrentFileParser:
    @staticmethod
    def parse_torrent_file(file_path: str) -> TorrentMetaData:
        with open(file_path, "rb") as f:
            data = f.read()

        decoded = bencodepy.decode(data)

        announce_url = decoded[b"announce"].decode("utf-8")
        info_dict = decoded[b"info"]
        piece_length = info_dict[b"piece length"]
        pieces = info_dict[b"pieces"]
        name = info_dict[b"name"].decode("utf-8")
        files = TorrentFileParser.parse_files(info_dict)
        torrent_meta = TorrentMetaData(
            announce_url, piece_length, pieces, name, files
        )
        torrent_meta.info_hash = InfoHash.get_info_hash(bencodepy.encode(info_dict))
        torrent_meta.piece_hash = PieceHash.get_piece_hash(pieces, 20)
        return torrent_meta

    @staticmethod
    def parse_files(info_dict):
        files = []
        if b"files" in info_dict:
            for file_entry in info_dict[b"files"]:
                length = file_entry[b"length"]
                path_segments = [p.decode("utf-8") for p in file_entry[b"path"]]
                file_path = os.path.join(*path_segments)
                files.append(TorrentFile(file_path, length))
        else:
            file_path = info_dict[b"name"].decode("utf-8")
            length = info_dict[b"length"]
            files.append(TorrentFile(file_path, length))
        return files
