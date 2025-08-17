import socket
import struct
import time
from message import Message, MessageType
from bittorrent_handshake import BitTorrentHandShake


class PieceDownloader:
    def __init__(self, torrent_metadata, index, peer_ip, peer_port, peer_id, final_file: bytearray):
        self.torrent_metadata = torrent_metadata
        self.index = index
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.peer_id = peer_id
        self.final_file = final_file
        self.download_successful = False

    def is_download_successful(self):
        return self.download_successful

    def download_piece(self):
        try:
            with socket.create_connection((self.peer_ip, self.peer_port)) as sock:
                handshake = BitTorrentHandShake(self.torrent_metadata.info_hash, self.peer_id, sock)
                handshake.do_handshake()

                if not self._wait_for_unchoke(sock):
                    return

                piece_data = self._start_download(sock)

                if piece_data is not None:
                    self._process_payload(piece_data)
                    self.download_successful = True

        except Exception as e:
            raise RuntimeError(f"Download failed: {e}")

    def _wait_for_unchoke(self, sock, timeout=100):
        start_time = time.time()

        while time.time() - start_time < timeout:
            msg = self._receive_message(sock)
            if msg.type == MessageType.UNCHOKE:
                return True
            time.sleep(0.2)
        return False

    def _receive_message(self, sock):
        raw_len = sock.recv(4)
        if len(raw_len) < 4:
            raise IOError("Failed to read message length")
        length = struct.unpack(">I", raw_len)[0]

        if length == 0:
            return Message(MessageType.KEEP_ALIVE, None)

        type_byte = sock.recv(1)
        if len(type_byte) < 1:
            raise IOError("Failed to read message type")

        payload = b""
        if length > 1:
            payload = sock.recv(length - 1)

        return Message(type_byte[0], payload)

    def _start_download(self, sock):
        piece_index = self.index
        piece_size = len(self.torrent_metadata.pieces) // self.torrent_metadata.piece_length
        block_size = 1 << 14
        num_blocks = (piece_size + block_size - 1) // block_size
        block_offset = 0

        full_piece = bytearray(piece_size)

        for block_index in range(num_blocks):
            block_length = (piece_size % block_size) if block_index == num_blocks - 1 else block_size
            request_payload = self._create_request_payload(piece_index, block_offset, block_length)
            self._send_message(MessageType.REQUEST, request_payload, sock)

            piece_message = self._receive_message(sock)

            if piece_message.type == MessageType.PIECE:
                block_data = piece_message.payload
                full_piece[block_offset:block_offset + len(block_data)] = block_data
                block_offset += len(block_data)
            else:
                return None

        return bytes(full_piece)

    def _send_message(self, msg_type, payload, sock):
        if payload is None:
            payload = b""

        length = 1 + len(payload)
        message = struct.pack(">IB", length, msg_type.value) + payload
        sock.sendall(message)

    def _create_request_payload(self, piece_index, piece_offset, piece_size):
        return struct.pack(">III", piece_index, piece_offset, piece_size)

    def _process_payload(self, response):
        piece_index = self.index
        piece_size = len(self.torrent_metadata.pieces) // self.torrent_metadata.piece_length
        new_index = (piece_index + 1) * piece_size
        self.final_file[new_index:new_index + len(response)] = response
