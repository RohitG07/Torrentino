import requests
import urllib.parse


class TrackerRequest:
    @staticmethod
    def send_request(torrent_metadata, client_peer_id):
        try:
            tracker_url = torrent_metadata.announce_url
            info_hash = TrackerRequest.hex_string_convert(torrent_metadata.info_hash)
            peer_id = client_peer_id
            port = 6969
            uploaded = 0
            downloaded = 0
            left = len(torrent_metadata.pieces)

            url = TrackerRequest.build_url(
                tracker_url, info_hash, peer_id, port, uploaded, downloaded, left
            )
            print("Tracker URL is", tracker_url)
            response = TrackerRequest.send_get_url(url)
            return response
        except Exception as e:
            raise RuntimeError(e)

    @staticmethod
    def send_get_url(query_url):
        response = requests.get(query_url)
        if response.status_code == 200:
            return response.text
        else:
            print("GET request failed")
            return None

    @staticmethod
    def build_url(tracker_url, info_hash, peer_id, port, uploaded, downloaded, left):
        params = {
            "info_hash": info_hash,
            "peer_id": peer_id,
            "port": port,
            "uploaded": uploaded,
            "downloaded": downloaded,
            "left": left,
        }
        return f"{tracker_url}?{urllib.parse.urlencode(params)}"

    @staticmethod
    def hex_string_convert(byte_data):
        return "".join(f"{b:02x}" for b in byte_data)
