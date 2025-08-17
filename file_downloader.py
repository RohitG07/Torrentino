from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from piece_downloader import PieceDownloader


class FileDownloader:
    THREAD_COUNT = 8

    def __init__(self, peers, torrent_metadata, peer_id: bytes):
        self.peers = peers
        self.torrent_metadata = torrent_metadata
        self.peer_id = peer_id

        # Final file buffer, size = total length of all pieces
        pieces = self.torrent_metadata.get_pieces()
        self.final_file = bytearray(len(pieces))

    def download_file(self):
        peer_count = len(self.peers)
        piece_count = len(self.torrent_metadata.get_pieces()) // self.torrent_metadata.get_piece_length()

        futures = []
        with ThreadPoolExecutor(max_workers=self.THREAD_COUNT) as executor:
            for index in range(piece_count):
                peer = self.peers[index % peer_count]
                futures.append(
                    executor.submit(
                        ThreadRunner(peer.ip, peer.port, self.peer_id, self.torrent_metadata, index, self.final_file).call
                    )
                )

            time.sleep(0.1)

            for future in as_completed(futures):
                try:
                    success = future.result()
                    if not success:
                        print("Unable to download the file")
                        return
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    raise

        print("File Downloaded Successfully")

    def get_final_file(self) -> bytes:
        return bytes(self.final_file)


class ThreadRunner:
    def __init__(self, peer_ip: str, peer_port: int, peer_id: bytes, torrent_metadata, index: int, final_file: bytearray):
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.peer_id = peer_id
        self.torrent_metadata = torrent_metadata
        self.index = index
        self.final_file = final_file

    def call(self) -> bool:
        tries_left = 5
        piece_downloader = PieceDownloader(self.torrent_metadata, self.index, self.peer_ip, self.peer_port, self.peer_id, self.final_file)

        while tries_left > 0 and not piece_downloader.is_download_successful():
            tries_left -= 1
            piece_downloader.download_piece()

        return piece_downloader.is_download_successful()
