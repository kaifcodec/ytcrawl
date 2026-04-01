import requests
import time
from generator import get_initial_token
from parser import CommentParser


class YTScraper:
    def __init__(self, video_id):
        self.video_id = video_id
        self.api_url = "https://www.youtube.com/youtubei/v1/next"
        self.api_key = "AIzaSyAO_xfS9Vm3sciq76v_S_x656W6mHqCg"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
            "Content-Type": "application/json",
        })

    def fetch(self, token):
        payload = {
            "context": {"client": {"clientName": "MWEB", "clientVersion": "2.20240328.00.00"}},
            "continuation": token
        }
        r = self.session.post(
            f"{self.api_url}?key={self.api_key}", json=payload)
        return r.json()

    def start(self, limit=5):
        token = get_initial_token(self.video_id)

        for page in range(limit):
            print(f"Page {page+1}...")
            data = self.fetch(token)
            comments, token = CommentParser.extract_batch(data)

            if not comments:
                print("No more comments found.")
                break

            for c in comments:
                print(f"[{c['type']}] {c['author']}: {c['text']}")

            if not token:
                print("\nEnd of thread")
                break

            time.sleep(0.5)


if __name__ == "__main__":
    vid = input("Enter YouTube Video ID: ")
    app = YTScraper(vid)
    app.start()
