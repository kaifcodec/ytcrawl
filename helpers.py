import json
from urllib.parse import urlparse, parse_qs

def extract_video_id(input_str):
    if "youtube.com" in input_str or "youtu.be" in input_str:
        parsed = urlparse(input_str)
        if parsed.hostname == "youtu.be":
            return parsed.path[1:]
        if "/shorts/" in parsed.path:
            return parsed.path.split("/shorts/")[1].split("/")[0]
        query = parse_qs(parsed.query)
        return query.get("v", [None])[0]
    return input_str

def clean_unicode(text):
    if isinstance(text, str) and ("\\u" in text or "\\ud" in text):
        try:
            return bytes(text, "utf-8").decode("unicode_escape")
        except:
            return text
    return text

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
