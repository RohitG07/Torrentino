class TorrentFile:
    def __init__(self, path, length):
        self.path = path
        self.length = length

    def get_path(self):
        return self.path

    def get_length(self):
        return self.length
