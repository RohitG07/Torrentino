class BencodingDecoder:
    def __init__(self):
        self.info = None   # raw info section
        self.pieces = None # raw pieces section

    def decode(self, data: bytes, index: list):
        if not data or index[0] >= len(data):
            return None

        char = data[index[0]]

        if char == ord('i'):
            end_index = data.index(b'e', index[0])
            number = int(data[index[0] + 1:end_index].decode())
            index[0] = end_index + 1
            return number

        elif char == ord('l'):
            index[0] += 1
            result = []
            while data[index[0]] != ord('e'):
                result.append(self.decode(data, index))
            index[0] += 1
            return result

        elif char == ord('d'):
            index[0] += 1
            result = {}
            while data[index[0]] != ord('e'):
                key = self.decode(data, index)
                value = self.decode(data, index)

                if isinstance(key, bytes):
                    key_str = key.decode(errors="ignore")
                    if key_str == "info":
                        self.info = data
                    elif key_str == "pieces":
                        self.pieces = data

                result[key] = value

            index[0] += 1
            return result

        elif chr(char).isdigit():
            colon_index = data.index(b':', index[0])
            length = int(data[index[0]:colon_index].decode())
            start = colon_index + 1
            end = start + length
            result = data[start:end]
            index[0] = end
            return result

        return None

    def get_info(self) -> bytes:
        return self.info

    def get_pieces(self) -> bytes:
        return self.pieces
