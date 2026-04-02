import requests
import time
from generator import get_initial_token
from parser import CommentParser
from helpers import clean_unicode, load_json, save_json

class YTScraper:
    def __init__(self, video_id, output, verbose=False, minimal=False):
        self.video_id = video_id
        self.output = output
        self.verbose = verbose
        self.minimal = minimal
        self.api_url = "https://www.youtube.com/youtubei/v1/next"
        self.api_key = "AIzaSyAO_xfS9Vm3sciq76v_S_x656W6mHqCg"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
            "Content-Type": "application/json",
        })

    def fetch(self, token):
        payload = {
            "context": {"client": {"clientName": "MWEB", "clientVersion": "2.20240328.00.00"}},
            "continuation": token
        }
        r = self.session.post(f"{self.api_url}?key={self.api_key}", json=payload)
        return r.json()

    def process_and_save(self, comments):
        fixed_comments = []
        for c in comments:
            new_c = {k: (clean_unicode(v) if k != "pfp_url" else v) 
                     for k, v in c.items() 
                     if not (k == "pfp_url" and not self.verbose) and not (self.minimal and k == "type")}
            fixed_comments.append(new_c)

        existing = load_json(self.output)
        existing.extend(fixed_comments)
        save_json(self.output, existing)

    def start(self, limit=5):
        token = get_initial_token(self.video_id)
        total_comments = 0

        for page in range(limit):
            print(f"Page {page + 1}...")
            data = self.fetch(token)
            comments, token = CommentParser.extract_batch(data)

            if not comments:
                print("No more comments found.")
                break

            for c in comments:
                print(f"[{c['type']}] {c['author']}: {c['text']}")
                if self.verbose and c.get("pfp_url"):
                    print(f"        └── PFP url: {c['pfp_url']}")
                if c.get("replyCount"):
                    print(f"        └── Reply count(s): {c['replyCount']}")
                if c.get("likes"):
                    print(f"        └── Like count(s): {c['likes']}")
                print()

            self.process_and_save(comments)
            total_comments += len(comments)
            if not token:
                print("End of thread")
                break
            time.sleep(0.5)

        print(f"\nTotal comments extracted: {total_comments}")
