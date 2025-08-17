class PeerInfo:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

    def get_ip(self) -> str:
        return self.ip

    def get_port(self) -> int:
        return self.port

    def __str__(self) -> str:
        return f"PeerInfo{{ip={self.ip}, port={self.port}}}"
