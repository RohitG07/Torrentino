import socket
import struct


class BitTorrentHandShake:
    def __init__(self, info_hash: bytes, peer_id: bytes, sock: socket.socket):
        self.info_hash = info_hash
        self.peer_id = peer_id
        self.socket = sock

    def do_handshake(self):
        try:
            if self._do_handshake(self.socket):
                print("Handshake successful")
            else:
                print("Handshake failed")
        except Exception as e:
            raise RuntimeError(f"Handshake error: {e}")

    def _do_handshake(self, sock: socket.socket) -> bool:
        protocol_identifier = b"BitTorrent protocol"
        pstrlen = len(protocol_identifier)  # should be 19
        reserved = b"\x00" * 8

        handshake_msg = struct.pack("!B", pstrlen) + protocol_identifier + reserved + self.info_hash + self.peer_id
        sock.sendall(handshake_msg)

        response = self._recv_all(sock, 68)

        return self._verify_handshake_response(response)

    def _recv_all(self, sock: socket.socket, length: int) -> bytes:
        data = b""
        while len(data) < length:
            chunk = sock.recv(length - len(data))
            if not chunk:
                raise ConnectionError("Connection closed during handshake")
            data += chunk
        return data

    def _verify_handshake_response(self, response: bytes) -> bool:
        received_info_hash = response[28:48]

        if received_info_hash != self.info_hash:
            print("infoHash mismatch")
            return False

        return True
