import json
from typing import List
from peer_info import PeerInfo


class PeerInfoParser:
    def __init__(self, response: str):
        self.response = response
        self.interval: int = 0
        self.peers: List[PeerInfo] = []

    def parse_tracker_info(self):
        data = json.loads(self.response)

        if "interval" in data:
            self.interval = data["interval"]

        if "peers" in data:
            peers_blob = data["peers"]
            self.peers = self._parse_peers_blob(peers_blob)

    def _parse_peers_blob(self, peers_blob: str) -> List[PeerInfo]:
        peer_list = []
        for i in range(0, len(peers_blob), 12):
            ip_hex = peers_blob[i:i+8]
            port_hex = peers_blob[i+8:i+12]

            ip_int = int(ip_hex, 16)
            port = int(port_hex, 16)

            ip_address = "{}.{}.{}.{}".format(
                (ip_int >> 24) & 0xFF,
                (ip_int >> 16) & 0xFF,
                (ip_int >> 8) & 0xFF,
                ip_int & 0xFF
            )

            peer_list.append(PeerInfo(ip_address, port))

        return peer_list

    def get_peers(self) -> List[PeerInfo]:
        return self.peers

    def get_interval(self) -> int:
        return self.interval

    def get_response(self) -> str:
        return self.response
