import os
import sys
import hashlib
import secrets

from bencoding_decoder import BencodingDecoder
from torrent_file_parser import TorrentFileParser
from tracker_request import TrackerRequest
from file_downloader import FileDownloader


class Main:
    peer_id: bytes = None

    @staticmethod
    def main(args):
        if len(args) < 2:
            print("unequal argument")
            return

        command = args[0]

        if command == "decode":
            raw_str = args[1].encode("utf-8")
            decoder = BencodingDecoder()
            decoded_value = decoder.decode(raw_str, pos=0)
            print(f"object type is {type(decoded_value)} object value is {decoded_value}")

        elif command == "parse":
            for i, file in enumerate(args[1:], start=1):
                meta = TorrentFileParser.parse_torrent_file(file)
                if meta:
                    print(f"{i} - torrent file is {meta}")
                    print(f"infoHash is {Main.hex_string_convert(meta.info_hash)}")
                else:
                    print(f"Unable to parse file - {file}")

        elif command == "download":
            Main.peer_id = Main.generate_id()
            for file in args[1:]:
                meta = TorrentFileParser.parse_torrent_file(file)
                if meta:
                    peer_info = TrackerRequest.send_request(meta, Main.hex_string_convert(Main.peer_id))
                    peers = peer_info.get_peers()
                    FileDownloader(peers, meta, Main.peer_id)
                else:
                    print(f"Unable to download file {file}")

    @staticmethod
    def generate_id() -> bytes:
        return secrets.token_bytes(20)

    @staticmethod
    def hex_string_convert(b: bytes) -> str:
        return b.hex()


if __name__ == "__main__":
    Main.main(sys.argv[1:])
